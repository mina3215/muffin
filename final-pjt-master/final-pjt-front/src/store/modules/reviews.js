import axios from 'axios'
import router from '../../router'

const API_URL = 'http://127.0.0.1:8000/muffins/';

const reviews = {
  namespaced: true,
  state: {
    movie_reviews: [],
    review_author: [],
    comment_author: [],
    commented_review: [],
    review_comments : [],
    boardmovie_info : {
      'title' : '',
      'img_path' : '',
  }
  },
  getters: {},
  mutations: {
    // 리뷰 가져오기
    GET_REVIEWS(state, reviews) {
      state.movie_reviews = reviews
    }
    ,
    GET_REVIEWCOMMENTS(state,comments){
      console.log("커밋됐냐?????")
      console.log(comments)
      console.log('겟리뷰코멘츠뮤테이션성공')
      state.review_comments = comments
      
    },
  },
  actions: {

    // 리뷰 가져오기
    getReviews(context) {
      const movieId = router.currentRoute.params.id;
      axios({
        method: 'get',
        url: `${API_URL}movies/${movieId}/reviews/`
      })
        .then(res => {
          context.commit('GET_REVIEWS', res.data)
        })
        .catch(err => {
          console.log(err)
        })
    },
  }
}

export default reviews
