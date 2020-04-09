module.exports = {
    title:'Kotidostories',
    description: 'Kotidostories API documentation',
    themeConfig: {
        nav: [
            { text: 'Home', link: '/' },
            { text: 'Guide', link: '/guide/' },
            { text: 'External', link: 'https://google.com' }
          ],
        sidebar:{
          '/guide/':[
            '',
            'endpoints',
            'database'
          ]
        }
      },
}