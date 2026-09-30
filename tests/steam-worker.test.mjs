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
