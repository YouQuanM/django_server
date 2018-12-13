import Vue from 'vue'
import Router from 'vue-router'
import index from '@/components/index'
import marticle from '@/components/marticle'
import writeArticle from '@/components/writeArticle'
import logUp from '@/components/logUp'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/index',
      name: 'index',
      component: index
    },
    {
      path: '/marticle',
      name: 'marticle',
      component: marticle
    },
    {
      path: '/writeArticle',
      name: 'writeArticle',
      component: writeArticle
    },
    {
      path: '/logUp',
      name: 'logUp',
      component: logUp
    }
  ]
})
