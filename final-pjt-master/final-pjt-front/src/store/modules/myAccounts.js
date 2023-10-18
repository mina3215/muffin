import axios from 'axios'
import router from '../../router'
// import createPersistedState from 'vuex-persistedstate'
const API_URL = 'http://127.0.0.1:8000/'

const myAccounts = {
  // plugins:[
  //   // localstorage에 token 넣기 
  //   createPersistedState
  // ],
  namespaced: true,
  state : {
    recommend_list : null,
    token: null,
    username: null,
    my_genre : null,
    prizes : [0, false, false, false, false],
  },
  getters:{
    isLogin(state){
      return state.token ? true : false
    }
  },
  mutations : {
    SAVE_TOKEN(state, token) {
      state.token = token
      router.push('/')
    },
    SAVE_USER(state, username){
      state.username = username
    },
    SAVE_RECO(state, recommend){
      state.recommend_list = recommend
    },
    SAVE_GENRE(state, genre){
      state.my_genre = genre
    },
    SAVE_PRIZE(state, prize){
      for(let i=0; i<prize.length; i++){
        state.prizes[prize[i].id] = true
      }
      console.log(state.prizes)
    }


  },
  actions : {
    signup(context, payload){
      const username = payload.username
      const password1 = payload.password1
      const password2 = payload.password2
      // console.log('여긴 도달')
      axios({
        method: 'post',
        url: `${API_URL}accounts/signup/`,
        data: {
          username, password1, password2
        }
      })
        .then((res) => {
          console.log(res.data)
          router.push('/')
        })
        .catch((err) => 
        console.log(err),
        )
    },
    
    login(context, payload) {
      const username = payload.username
      const password = payload.password
      // console.log(username)
      axios({
        method: 'post',
        url: `${API_URL}accounts/login/`,
        data: {
          username, password
        }
      })
        .then((res) => {
          context.commit('SAVE_USER', payload.username)
          context.dispatch('getrecommend')
          console.log(res)
          context.commit('SAVE_TOKEN', res.data.key)
        })
        .catch((err) => 
        console.log(err,'멍청이')
        // alert("아이디 혹은 비밀번호가 틀렸습니다.")
        )
    },  
    getrecommend(context){
      const username = context.state.username
      axios({
        method: 'get',
        url: `${API_URL}muffins/recommend/${username}/`
      })
      .then((res) => {
        console.log(res)
        context.commit('SAVE_PRIZE', res.data['prizes'])
        context.commit('SAVE_RECO', res.data['recommendation']);
        context.commit('SAVE_GENRE', res.data['my_Genre']);
      })
    }
  }
}

export default myAccounts