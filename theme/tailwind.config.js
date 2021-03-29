module.exports = {
  future: {
      removeDeprecatedGapUtilities: true,
      purgeLayersByDefault: true,
  },
  purge: {
      enabled: false, //true for production build
      content: [
          '../**/templates/*.html',
          '../**/templates/**/*.html'
      ]
  },
  theme: {
    fontSize: {
        'normal': '1rem',
        'lg': ['1.125rem', {
          lineHeight: '1.75rem',
        }],
        'xl': ['1.25rem', {
          lineHeight: '1.75rem',
        }],
        '2xl': ['1.5rem', {
          lineHeight: '2rem',
        }],
        '3xl': ['1.875rem', {
          lineHeight: '2.25rem',
        }],
        '4xl': ['2.25rem', {
          lineHeight: '2.5rem',
        }],
        '5xl': ['3rem',{lineHeight:'1'}],
        '6xl':['3.7rem',{lineHeight:'1'}],
        '7xl':['4.5rem',{lineHeight:'1'}],
    
        'xl-3':['3.5rem',{lineHeight:'1'}],

        'subtitle':['1.4rem'],
        'title':['1.6rem']
    },
    
    extend: {
      gridTemplateColumns: {
       '4-auto': 'auto auto auto auto',
       '3-auto': 'auto auto auto',
      },
      fontFamily: {
        'ebrima': ['Ebrima', 'Roboto', 'Arial', 'sans-serif'],
        'ebrima-bold': ['EbrimaBold', 'Roboto', 'Arial', 'sans-serif'],
      },
      width:{
        'fit-content' : 'fit-content',
        'x60': '60%',
        '25rem': '25rem',
        '30rem': '30rem',
        '2vw': '2vw',
      },
      letterSpacing: {
        '.2em' : '.2em',
        '.3em' : '.3em',
        '1em' : '1em'
      },
      backgroundColor: {
        'primary': '#00325b',
        'accent': '#5cbcfd'
      },
      textColor: {
        'accent': '#5cbcfd',
        'default': '#363636',
      },
      flex:{
        '2':'2',
      }
    },
  },
  variants: {},
  plugins: [],
}