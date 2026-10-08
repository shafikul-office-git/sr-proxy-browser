import { defineComponent, h } from 'vue'

const paths = {
  Users: [
    ['path', { d: 'M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2' }],
    ['circle', { cx: '9', cy: '7', r: '4' }],
    ['path', { d: 'M22 21v-2a4 4 0 0 0-3-3.87' }],
    ['path', { d: 'M16 3.13a4 4 0 0 1 0 7.75' }],
  ],
  Play: [['polygon', { points: '5 3 19 12 5 21 5 3' }]],
  ShieldCheck: [
    ['path', { d: 'M20 13c0 5-3.5 7.5-8 9-4.5-1.5-8-4-8-9V5l8-3 8 3v8Z' }],
    ['path', { d: 'm9 12 2 2 4-4' }],
  ],
  Zap: [['polygon', { points: '13 2 3 14 12 14 11 22 21 10 12 10 13 2' }]],
  Search: [
    ['circle', { cx: '11', cy: '11', r: '8' }],
    ['path', { d: 'm21 21-4.3-4.3' }],
  ],
  Activity: [['polyline', { points: '22 12 18 12 15 21 9 3 6 12 2 12' }]],
  Rocket: [
    ['path', { d: 'M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09Z' }],
    ['path', { d: 'm12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6.05 11a22.35 22.35 0 0 1-3.95 2Z' }],
    ['path', { d: 'M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0' }],
    ['path', { d: 'M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5' }],
    ['circle', { cx: '16', cy: '6', r: '1' }],
  ],
  Plus: [['path', { d: 'M5 12h14' }], ['path', { d: 'M12 5v14' }]],
  X: [['path', { d: 'M18 6 6 18' }], ['path', { d: 'm6 6 12 12' }]],
  ExternalLink: [
    ['path', { d: 'M15 3h6v6' }],
    ['path', { d: 'M10 14 21 3' }],
    ['path', { d: 'M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6' }],
  ],
  Pencil: [
    ['path', { d: 'M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.638a.5.5 0 0 0 .62.62l4.638-1.321a2 2 0 0 0 .83-.5z' }],
    ['path', { d: 'm15 5 4 4' }],
  ],
  SlidersHorizontal: [
    ['line', { x1: '21', x2: '14', y1: '4', y2: '4' }],
    ['line', { x1: '10', x2: '3', y1: '4', y2: '4' }],
    ['line', { x1: '21', x2: '12', y1: '12', y2: '12' }],
    ['line', { x1: '8', x2: '3', y1: '12', y2: '12' }],
    ['line', { x1: '21', x2: '16', y1: '20', y2: '20' }],
    ['line', { x1: '12', x2: '3', y1: '20', y2: '20' }],
    ['line', { x1: '14', x2: '14', y1: '2', y2: '6' }],
    ['line', { x1: '8', x2: '8', y1: '10', y2: '14' }],
    ['line', { x1: '16', x2: '16', y1: '18', y2: '22' }],
  ],
  Fingerprint: [
    ['path', { d: 'M12 11a4 4 0 0 1 4 4c0 3.5-1.5 6-4 8' }],
    ['path', { d: 'M8 15a4 4 0 0 1 8 0c0 2.5-.7 4.6-2 6' }],
    ['path', { d: 'M12 3a9 9 0 0 0-9 9' }],
    ['path', { d: 'M12 7a5 5 0 0 0-5 5' }],
    ['path', { d: 'M12 19a4 4 0 0 0 4-4' }],
    ['path', { d: 'M17 12a5 5 0 0 1 2 4' }],
    ['path', { d: 'M3 16a9 9 0 0 0 2 5' }],
  ],
  Globe: [
    ['circle', { cx: '12', cy: '12', r: '10' }],
    ['line', { x1: '2', x2: '22', y1: '12', y2: '12' }],
    ['path', { d: 'M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10Z' }],
  ],
  Lock: [
    ['rect', { width: '18', height: '11', x: '3', y: '11', rx: '2' }],
    ['path', { d: 'M7 11V7a5 5 0 0 1 10 0v4' }],
  ],
  ArrowLeft: [['path', { d: 'm12 19-7-7 7-7' }], ['path', { d: 'M19 12H5' }]],
  ChevronDown: [['path', { d: 'm6 9 6 6 6-6' }]],
}

function makeIcon(name) {
  return defineComponent({
    name,
    inheritAttrs: false,
    setup(_, { attrs }) {
      return () => h('svg', {
        ...attrs,
        xmlns: 'http://www.w3.org/2000/svg',
        width: 24,
        height: 24,
        viewBox: '0 0 24 24',
        fill: 'none',
        stroke: 'currentColor',
        'stroke-width': 2,
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
      }, paths[name].map(([tag, props]) => h(tag, props)))
    },
  })
}

export const Users = makeIcon('Users')
export const Play = makeIcon('Play')
export const ShieldCheck = makeIcon('ShieldCheck')
export const Zap = makeIcon('Zap')
export const Search = makeIcon('Search')
export const Activity = makeIcon('Activity')
export const Rocket = makeIcon('Rocket')
export const Plus = makeIcon('Plus')
export const X = makeIcon('X')
export const ExternalLink = makeIcon('ExternalLink')
export const Pencil = makeIcon('Pencil')
export const SlidersHorizontal = makeIcon('SlidersHorizontal')
export const Fingerprint = makeIcon('Fingerprint')
export const Globe = makeIcon('Globe')
export const Lock = makeIcon('Lock')
export const ArrowLeft = makeIcon('ArrowLeft')
export const ChevronDown = makeIcon('ChevronDown')
