import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ActorView from '../views/ActorView.vue'
import MovieDetailView from '../views/MovieDetailView.vue'
import ProfileView from '../views/ProfileView.vue'
import ReviewBoard from '../views/ReviewBoard.vue'
import ReviewForm from '../views/ReviewForm.vue'
import ReviewEditForm from '../views/ReviewEditForm.vue'
import ReviewDetailView from '../views/ReviewDetailView.vue'
import LoginPage from '../views/LoginPage.vue'
import SignupPage from '../views/SignupPage.vue'
import SearchPage from '../views/SearchView.vue'
import ActorDetailPage from '../views/ActorBoard.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/actor',
    name: 'actor',
    component: ActorView
  }
  ,
  {
    path: '/moviedetail/:id',
    name: 'moviedetail',
    component: MovieDetailView
  },
  {
    path: '/profile/:username',
    name: 'profile',
    component: ProfileView
  },
  {
    path: '/reviewboard/:id',
    name: 'reviewboard',
    component: ReviewBoard
  },
  {
    path: '/reviewboard/:id/form/',
    name: 'reviewboardform',
    component: ReviewForm
  },
  {
    path: '/reviewboard/:id/detail/:reviewId/',
    name: 'reviewboarddetail',
    component: ReviewDetailView
  },
  {
    path: '/reviewboard/:id/form/:reviewId/',
    name: 'revieweditform',
    component:ReviewEditForm
  },
  {
    path: '/loginpage',
    name: 'loginpage',
    component: LoginPage
  },
  {
    path: '/signuppage',
    name: 'signuppage',
    component: SignupPage
  },
  {
    path: '/search/:keyword',
    name: 'search',
    component :SearchPage,
    props:true
  },
  {
    path: '/actor/:id',
    name: 'actordetail',
    component :ActorDetailPage,
    props:true
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
