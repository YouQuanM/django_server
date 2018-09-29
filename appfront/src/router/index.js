import Vue from 'vue'
import Router from 'vue-router'
import library from '@/components/library'
import article from '@/components/article'
import userpage from '@/components/userpage'

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
    },
    {
      path: '/userpage',
      name: 'userpage',
      component: userpage
    }
  ]
})
