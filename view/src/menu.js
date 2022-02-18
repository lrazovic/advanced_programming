import {
  mdiAccountCircle, mdiFormatListBulleted, mdiNewspaper
} from '@mdi/js'

export default [
  // 'General',
  [
    {
      to: '/',
      icon: mdiNewspaper,
      label: 'Feed'
    },
    {
      to: '/profile',
      icon: mdiAccountCircle,
      label: 'My profile'
    },
    {
      to: '/source-list',
      icon: mdiFormatListBulleted,
      label: 'Manage news sources'
    }
  ]
]
