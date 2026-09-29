import rss from '@astrojs/rss'
import { notes } from '../lib/content'
export function GET() {
  return rss({
    title: 'sychostar', description: '课程笔记、技术积累与阅读记录',
    site: 'https://lihaoze-bob.github.io',
    items: notes.map(note => ({ title: note.title, pubDate: new Date(note.publishedAt!),
      description: note.description || note.cardHeadings?.join(' · ') || note.title, link: note.url }))
  })
}
