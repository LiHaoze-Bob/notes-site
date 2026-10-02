import assert from 'node:assert/strict'
import test from 'node:test'

import worker, { profileData, statsData } from '../workers/steam/worker.mjs'

const STEAM_ID = '76561199304157766'

test('profile data keeps only the configured public profile', () => {
  const profile = profileData({
    steamid: STEAM_ID,
    personaname: 'Player',
    communityvisibilitystate: 3,
    personastate: 1,
    gameid: '123',
    gameextrainfo: 'Game',
    avatarfull: 'https://avatars.steamstatic.com/avatar.jpg',
  }, '2026-09-30T00:00:00.000Z')
  assert.equal(profile.status, 'in-game')
  assert.equal(profile.currentGame, 'Game')
  assert.equal(profile.updatedAt, '2026-09-30T00:00:00.000Z')
  assert.throws(() => profileData({ steamid: 'other', personaname: 'Other' }))
})

test('private profiles expose no game or status details', () => {
  const profile = profileData({
    steamid: STEAM_ID,
    personaname: 'Private',
    communityvisibilitystate: 1,
    personastate: 1,
    gameid: '123',
    gameextrainfo: 'Hidden Game',
  })
  assert.equal(profile.status, 'unknown')
  assert.equal(profile.currentGame, '')
})

test('statistics sum all recent games before selecting three covers', () => {
  const stats = statsData(
    { player_level: 12, badges: [{}, {}] },
    { game_count: 40 },
    { total_count: 4, games: [1, 2, 3, 4].map(appid => ({ appid, name: `Game ${appid}`, playtime_2weeks: 30, playtime_forever: 60 })) },
    '2026-09-30T00:00:00.000Z',
  )
  assert.equal(stats.recentHours, 2)
  assert.equal(stats.recentGames.length, 3)
  assert.equal(stats.games, 40)
  assert.equal(stats.updatedAt, '2026-09-30T00:00:00.000Z')
})

test('endpoint rejects other origins and paths without contacting Steam', async () => {
  const env = { STEAM_API_KEY: 'unused' }
  const forbidden = await worker.fetch(new Request('https://example.workers.dev/steam', {
    headers: { Origin: 'https://other.example' },
  }), env)
  assert.equal(forbidden.status, 403)
  const missing = await worker.fetch(new Request('https://example.workers.dev/other'), env)
  assert.equal(missing.status, 404)
  const unconfigured = await worker.fetch(new Request('https://example.workers.dev/steam'), {})
  assert.equal(unconfigured.status, 503)
  const preflight = await worker.fetch(new Request('https://example.workers.dev/steam', {
    method: 'OPTIONS', headers: { Origin: 'https://lihaoze-bob.github.io' },
  }), env)
  assert.equal(preflight.status, 204)
  assert.equal(preflight.headers.get('Access-Control-Allow-Origin'), 'https://lihaoze-bob.github.io')
})

function mockUpstream(t, respond) {
  const previous = globalThis.caches
  const entries = new Map()
  globalThis.caches = { default: {
    async match(request) { return entries.get(request.url)?.clone() },
    async put(request, response) { entries.set(request.url, response.clone()) },
    async delete(request) { return entries.delete(request.url) },
  } }
  t.after(() => { if (previous === undefined) delete globalThis.caches; else globalThis.caches = previous })
  t.mock.method(globalThis, 'fetch', respond)
  return entries
}

test('upstream authentication failure returns a safe diagnostic without the key', async t => {
  mockUpstream(t, async () => new Response('Forbidden', { status: 403 }))
  const response = await worker.fetch(new Request('https://example.workers.dev/steam'), { STEAM_API_KEY: 'secret-test-key' })
  assert.equal(response.status, 502)
  assert.deepEqual(await response.json(), { error: 'Steam temporarily unavailable', reason: 'steam_http_403' })
})

test('successful requests cache sanitized data and preserve collection timestamps', async t => {
  let calls = 0
  const entries = mockUpstream(t, async (input, options) => {
    calls++
    assert.equal(options.redirect, 'manual')
    const url = new URL(input)
    assert.equal(url.searchParams.get('key'), 'secret-test-key')
    if (url.pathname.includes('GetPlayerSummaries')) {
      return Response.json({ response: { players: [{ steamid: STEAM_ID, personaname: 'Player', communityvisibilitystate: 3, personastate: 1 }] } })
    }
    const parameters = JSON.parse(url.searchParams.get('input_json'))
    assert.equal(parameters.steamid, STEAM_ID)
    return Response.json({ response: url.pathname.includes('GetBadges') ? { player_level: 12, badges: [] }
      : url.pathname.includes('GetOwnedGames') ? { game_count: 4 } : { total_count: 0, games: [] } })
  })
  const request = new Request('https://example.workers.dev/steam', { headers: { Origin: 'https://lihaoze-bob.github.io' } })
  const env = { STEAM_API_KEY: 'secret-test-key' }
  const first = await worker.fetch(request, env)
  assert.equal(first.status, 200)
  assert.equal(first.headers.get('Access-Control-Allow-Origin'), 'https://lihaoze-bob.github.io')
  const data = await first.json()
  assert.equal(data.status, 'online')
  assert.equal(data.stats.games, 4)
  assert.equal(data.stats.recentHours, 0)
  assert.deepEqual(await (await worker.fetch(request, env)).json(), data)
  assert.equal(calls, 4)
  for (const [key, value] of entries) {
    assert.ok(!key.includes('secret-test-key'))
    assert.ok(!(await value.clone().text()).includes('secret-test-key'))
  }
})

test('statistics failure still allows status refresh', async t => {
  mockUpstream(t, async input => new URL(input).pathname.includes('GetPlayerSummaries')
    ? Response.json({ response: { players: [{ steamid: STEAM_ID, personaname: 'Player', communityvisibilitystate: 3, personastate: 0 }] } })
    : new Response('Unavailable', { status: 503 }))
  const response = await worker.fetch(new Request('https://example.workers.dev/steam'), { STEAM_API_KEY: 'secret-test-key' })
  assert.equal(response.status, 200)
  const data = await response.json()
  assert.equal(data.status, 'offline')
  assert.equal(data.stats, null)
})

test('upstream redirects are rejected without forwarding credentials', async t => {
  let calls = 0
  mockUpstream(t, async (input, options) => {
    calls++
    assert.equal(options.redirect, 'manual')
    return new Response(null, { status: 302, headers: { Location: 'https://other.example/' } })
  })
  const response = await worker.fetch(new Request('https://example.workers.dev/steam'), { STEAM_API_KEY: 'secret-test-key' })
  assert.equal(response.status, 502)
  assert.equal((await response.json()).reason, 'steam_http_302')
  assert.equal(calls, 1)
})

test('unexpected errors redact credentials and URLs from logs and responses', async t => {
  let log = ''
  t.mock.method(console, 'warn', (...args) => { log = args.join(' ') })
  mockUpstream(t, async () => { throw new Error('Failed https://api.steampowered.com/?key=secret-test-key secret-test-key') })
  const response = await worker.fetch(new Request('https://example.workers.dev/steam'), { STEAM_API_KEY: 'secret-test-key' })
  assert.equal(response.status, 502)
  assert.ok(log.includes('[redacted]') && log.includes('[url]'))
  assert.ok(!log.includes('secret-test-key') && !log.includes('api.steampowered.com'))
  assert.ok(!(await response.text()).includes('secret-test-key'))
})
