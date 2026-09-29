import { readFileSync } from 'node:fs'

export interface NotePage {
  route: string
  url: string
  title: string
  html: string
  description?: string
  headings: { depth: number; slug: string; text: string }[]
  breadcrumbs: { title: string; url: string }[]
  directory?: string[]
  cardHeadings?: string[]
  publishedAt?: string
  updatedAt?: string
  tags?: string[] | string
  tagLinks?: { title: string; url: string }[]
  isNote: boolean
  folder_previous?: { title: string; url: string } | null
  folder_next?: { title: string; url: string } | null
}

const data = JSON.parse(readFileSync(process.env.ASTRO_CONTENT_FILE || '.runtime/astro-content.json', 'utf8'))
export const pages: NotePage[] = data.pages
export const notes = pages.filter(page => page.isNote).sort((a, b) =>
  Date.parse(b.publishedAt || '') - Date.parse(a.publishedAt || '') || a.route.localeCompare(b.route))
export const date = (value: string) => new Intl.DateTimeFormat('en-US', {
  month: 'short', day: 'numeric', year: 'numeric', timeZone: 'Asia/Shanghai'
}).format(new Date(value))
