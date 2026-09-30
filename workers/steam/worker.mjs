// Only this public profile is exposed. Never proxy caller-supplied URLs or Steam IDs.
const STEAM_ID = '76561199304157766'
const SITE_ORIGIN = 'https://lihaoze-bob.github.io'
const STATES = ['offline', 'online', 'busy', 'away', 'snooze', 'trade', 'play']

function number(value) {
  return typeof value === 'number' && Number.isFinite(value) && value >= 0 ? value : null
}

function avatar(value) {
  try {
    const url = new URL(value)
    return url.protocol === 'https:' && url.hostname.endsWith('.steamstatic.com') ? url.href : ''
  } catch { return '' }
}

export function profileData(player, now = new Date().toISOString()) {
  if (player?.steamid !== STEAM_ID || typeof player.personaname !== 'string') {
    throw new Error('Invalid Steam profile')
  }
  const isPublic = player.communityvisibilitystate === 3
  const currentGame = isPublic && player.gameid && typeof player.gameextrainfo === 'string' ? player.gameextrainfo : ''
  return {
    name: player.personaname, avatar: avatar(player.avatarfull), isPublic,
    status: !isPublic ? 'unknown' : currentGame ? 'in-game' : STATES[player.personastate] || 'unknown',
    currentGame, updatedAt: now,
  }
}

export function statsData(badges, owned, recent, now = new Date().toISOString()) {
  const games = Array.isArray(recent.games) ? recent.games : []
  const minutes = games.map(game => number(game.playtime_2weeks))
  return {
    level: number(badges.player_level),
    badges: Array.isArray(badges.badges) ? badges.badges.length : null,
    games: number(owned.game_count),
    // Sum every returned game, before selecting three covers. Missing playtime is not zero.
    recentHours: number(recent.total_count) !== null && minutes.every(value => value !== null)
      ? Math.round(minutes.reduce((sum, value) => sum + value, 0) / 6) / 10 : null,
    recentGames: games.filter(game => Number.isInteger(game.appid) && game.appid > 0 && typeof game.name === 'string')
      .slice(0, 3).map(game => ({
        appid: String(game.appid), name: game.name,
        image: `https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/${game.appid}/capsule_184x69.jpg`,
        hours: number(game.playtime_forever) === null ? null : Math.round(game.playtime_forever / 6) / 10,
      })),
    updatedAt: now,
  }
}

async function steam(method, parameters, key, service = 'IPlayerService') {
  const version = service === 'ISteamUser' ? 'v2' : 'v1'
  const url = new URL(`https://api.steampowered.com/${service}/${method}/${version}/`)
  url.searchParams.set('key', key)
  if (service === 'IPlayerService') url.searchParams.set('input_json', JSON.stringify(parameters))
  else for (const [name, value] of Object.entries(parameters)) url.searchParams.set(name, value)
  const response = await fetch(url, { signal: AbortSignal.timeout(5000), redirect: 'error' })
  if (!response.ok) throw new Error('Steam unavailable')
  const data = await response.json()
  if (!data.response || typeof data.response !== 'object') throw new Error('Invalid Steam response')
  return data.response
}

async function cached(cache, key, ttl, load) {
  const hit = await cache.match(key)
  if (hit) return hit.json()
  const data = await load()
  // Cache sanitized data only; cache keys and bodies never contain the API key.
  await cache.put(key, Response.json(data, { headers: { 'Cache-Control': `public, max-age=${ttl}` } }))
  return data
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url)
    const origin = request.headers.get('Origin')
    const allowed = (env.ALLOWED_ORIGINS || SITE_ORIGIN).split(',').map(value => value.trim())
    const headers = { 'Cache-Control': 'no-store', 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff' }
    if (origin && !allowed.includes(origin)) return Response.json({ error: 'Origin not allowed' }, { status: 403, headers })
    if (origin) headers['Access-Control-Allow-Origin'] = origin
    const reply = (data, status = 200) => Response.json(data, { status, headers })
    if (url.pathname !== '/steam' || url.search) return reply({ error: 'Not found' }, 404)
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: { ...headers, 'Access-Control-Allow-Methods': 'GET, OPTIONS' } })
    if (request.method !== 'GET') return reply({ error: 'Method not allowed' }, 405)
    if (!env.STEAM_API_KEY) return reply({ error: 'Steam service is not configured' }, 503)
    const cache = caches.default
    const profileKey = new Request(`${url.origin}/cache/v1/${STEAM_ID}/profile`)
    const statsKey = new Request(`${url.origin}/cache/v1/${STEAM_ID}/stats`)
    try {
      const profile = await cached(cache, profileKey, 30, async () => {
        const data = await steam('GetPlayerSummaries', { steamids: STEAM_ID }, env.STEAM_API_KEY, 'ISteamUser')
        return profileData(data.players?.[0])
      })
      if (!profile.isPublic) {
        await cache.delete(statsKey)
        return reply({ ...profile, stats: statsData({}, {}, {}, profile.updatedAt) })
      }
      let stats = null
      try {
        stats = await cached(cache, statsKey, 3600, async () => {
          const [badges, owned, recent] = await Promise.all([
            steam('GetBadges', { steamid: STEAM_ID }, env.STEAM_API_KEY),
            steam('GetOwnedGames', { steamid: STEAM_ID, include_appinfo: false, include_played_free_games: true }, env.STEAM_API_KEY),
            steam('GetRecentlyPlayedGames', { steamid: STEAM_ID, count: 0 }, env.STEAM_API_KEY),
          ])
          return statsData(badges, owned, recent)
        })
      } catch { /* Preserve the frontend's dated statistics; status can still refresh. */ }
      return reply({ ...profile, stats })
    } catch {
      // Never return/log upstream error text, which may include a URL containing the key.
      return reply({ error: 'Steam temporarily unavailable' }, 502)
    }
  },
}
