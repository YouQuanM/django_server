import Vue from 'vue'
import Router from 'vue-router'
import library from '@/components/library'
import article from '@/components/article'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/library',
      name: 'library',
      component: library
    },
    {
      path: '/article',
      name: 'article',
      component: article
    }
  ]
})
