import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import myAccounts from './modules/myAccounts.js'
import reviews from './modules/reviews.js'

// 데이터 유지를 위해 import
import createPersistedState from 'vuex-persistedstate';
// import router from '../router'

const API_URL = 'http://127.0.0.1:8000/muffins/'
Vue.use(Vuex)

export default new Vuex.Store({
  modules : {
    myAccounts,
    reviews,
  },
  state: {
    movies: [],
    comments: [],
    genres_movies : [],
    sorted_genres : [],
  },
  getters: {
  },
  mutations: {
    // 박스오피스 10개 받아오기
    GET_MOVIES(state, movies) {
      state.movies = movies
    },

    GET_COMMENTS(state,comments){
      console.log('겟코멘츠뮤테이션성공')

      state.comments = comments
    },
    GET_GENRE_MOVIES(state, genre_movie_list){
      state.genres_movies.push(genre_movie_list)
    }
  },
  actions: {
    // 박스오피스 10개 받아오기
    getMovies(context) {
      axios({
        method: 'get',
        url: `${API_URL}home/`,
      })
      .then((res) => {
        context.commit('GET_MOVIES', res.data)
      })
      .catch((err) => {
      console.log(err)
      })
    },

     // 한줄평 목록 받아오기
     getComments(context) {
      const movieId = this.$route.params.id; // 현재 라우트의 id 값 가져오기
      // console.log(movieId)
      axios({
        method: 'get',
        url: `${API_URL}comments/${movieId}`, // URL에 movieId 포함
      })
      .then((res) => {
        console.log('겟코멘츠액션성공')
        context.commit('GET_COMMENTS', res.data);
      })
      .catch((err) => {
        console.log('겟코멘츠액션에러')
        console.log(err);
      });
    },
    
    getgenremovies(context){
      const genre_pks = context.state.myAccounts.my_genre
      this.state.genres_movies = []
      let sortedData = Object.entries(genre_pks).sort(function(a, b) {
        return b[1] - a[1];
      });
      this.state.sorted_genres = sortedData
      // let movies_of_genre = []
      for(let i = 0; i < 3; i ++){
        const genre_pk = sortedData[i][0]
        console.log(genre_pk)
        axios({
          method: 'get',
          url: `${API_URL}movies/genre/${genre_pk}/`, // URL에 movieId 포함
        })
        .then((res) => {
          context.commit('GET_GENRE_MOVIES', res.data)
        })
        .catch((err) => {
          console.log(err, '바보냐 너');
        });
      }
    }
    },
    plugins: [
      createPersistedState()
    ],
})