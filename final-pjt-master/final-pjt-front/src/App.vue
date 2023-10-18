<template>
  <div class="app-parent">
    <div class="navbar-container">
      <!-- 네비게이션 바 -->
      <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container">
          <!-- 로그인 상태에 따른 프로필 및 로그아웃 버튼 -->
          <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
            <ul class="navbar-nav">
              <li class="nav-item d-flex nav-link" v-if="$store.state.myAccounts.token">
                <p class="m-auto"> </p>
                <router-link :to="{ name: 'profile', params: { username: $store.state.myAccounts.username }}" class="nav-link">프로필</router-link>
              </li>
              <li v-if="!$store.state.myAccounts.token" class="nav-item m-auto">
                <router-link to="/loginpage" class="nav-link .text-primary">로그인</router-link>
              </li>
              <li v-if="$store.state.myAccounts.token" class="nav-item">
                

                <div @click="logout">
                  <router-link to="/" class="nav-link mt-2">로그아웃</router-link>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>


    <div class="main-container" >
      <div class="nav-container">
        <!-- 네브컨테이너 내용 -->
        <router-link to="/" class="navbar-brand">
          <img src="@/assets/logo5.png" alt="" class="logo">
          </router-link>        <div class="d-flex align-items-center mt-5">
          <form v-if="$store.state.myAccounts.token" class="form-inline search-form" @submit.prevent="search">
            <div class="input-group">
              <input class="searchform form-control" type="search" placeholder="영화제목" aria-label="검색" v-model="keyword">
                <div class="input-group-append">
                <button class="btn btn-custom" type="submit" value="검색">
                  <i class="fa fa-search"></i>
                </button>
              </div>
            </div>
          </form>
        </div>     
        <hr>
        <p class="p-5"></p>
        <div calss="routerlinks">
          <hr>
        <router-link :to="{ name: 'home' }">
          <h2>HOME</h2>
        </router-link> <br>
        <hr>
        <router-link to="/actor"><h2> ACTOR</h2></router-link> <br>
      </div>
      </div>
      <div class="content-container p-5">
        <transition name="slide-fade" mode="out-in">
          <router-view></router-view>
        </transition>
      </div>



    </div>

    <!-- 모달 영역 -->
    <div class="modal" v-if="showModal">
    <div class="modal-content">
      <h3>업적 달성!</h3>
      <p>축하합니다! 특정 업적을 달성했습니다.</p>
      <button class="btn btn-outline-success" @click="hideModal ">닫기</button>
    </div>
    
  </div>

  </div>
</template>

<script>

export default {
  data() {
    return {
      keyword: '',
      showModal: false, 
      check_path : '',
      check_word : '',
      userinfo : null,}
  },
  name: 'App',
  created() {
    this.$store.dispatch('getMovies')

  },
  mounted() {

  },
  methods: {

    gotologin(){
      if(!this.$store.state.myAccounts.token){
      
      this.$router.push({
        name : 'loginpage'
      })
      
      }  
    
      
    
    },
    logout() {
      alert("정상적으로 로그아웃 되었습니다.")
      console.log('로그아웃!')
      window.localStorage.clear()
      this.$store.state.myAccounts.token = null
      this.$store.state.myAccounts.username = null
      this.$store.state.myAccounts.my_genre = null
      this.$store.state.myAccounts.prizes = [0, false, false, false, false],
      this.$store.state.genres_movies = []
      this.$store.state.sorted_genres = null
    },


    search() {
      const currentRoute = this.$router.currentRoute
      const keyword = this.keyword.trim()

      // 검색어가 비어있는 경우 중복 이동 방지
      if (!keyword) {
        return
      }

      // 현재 경로와 검색어가 이미 저장된 값과 동일한 경우 중복 이동 방지
      if (currentRoute.name === 'search' && currentRoute.params.keyword === keyword) {
        return
      }

      this.$router.push({ 
        name: 'search',
        params: { keyword: keyword }
      })

    },  
  }
}
</script>
<style scoped>

@font-face {
font-family: 'SUIT-Regular';
src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_suit@1.0/SUIT-Regular.woff2') format('woff2');
font-weight: normal;
font-style: normal;
}

@font-face {
font-family: 'LINESeedKR-Bd';
src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_11-01@1.0/LINESeedKR-Bd.woff2') format('woff2');
font-weight: 700;
font-style: normal;
}


.app-parent {
font-family: 'SUIT-Regular';
-webkit-font-smoothing: antialiased;
-moz-osx-font-smoothing: grayscale;
text-align: center;
width: 100%;
height: 100%;
background: linear-gradient(to bottom, #4a4454, #3A6796, #384354);
}
.logo {
  max-width: 100%;
  height: auto;
}

.navbar-container {
position: fixed;
top: 0;
width: 100%;
z-index: 1;
}

.main-container {
margin-top: 56px; /* 네비게이션 바 높이 */
display: flex;
height: calc(100vh - 56px);
}
.nav-container {
flex: 0 0 300px;
font-family: 'LINESeedKR-Bd';
color: #ffffff;
display: flex;
flex-direction: column;
justify-content: center;
align-items: center;
font-size: 32px;
background-color: rgba(37, 28, 71, 0.344);
padding: 10px;
box-sizing: border-box;
}
hr{
box-shadow: 0px 4px 7px rgb(249, 248, 248);;
width: 300px;
}
.nav-container h2 {
margin-bottom: 20px;
font-size: 28px;
}

.nav-container a {
color: #ffffff;
text-decoration: none;
transition: color 0.3s ease;
display: block;
}

.nav-container a:hover {
color: #b24eff;
}
.nav-container button {
/* height: 35px; */
color: #ffffff;
font-size: 25px;
background: darkcyan;
border: none;
cursor: pointer;
padding: 3px 0;
width: 100%;
}

.nav-container button:hover {
color: #7420b4;
}


.content-container {
flex: 1;
overflow-y: auto;
background: linear-gradient(to bottom, #4a445400, #3A6796, #38435400);
padding: 20px;
box-sizing: border-box;
}

.searchform {
height: 40px;
border-radius: 5px;
}

.search-form .input-group {

position: relative;
width: 100%;
}

.search-form .form-control {
padding-right: 50px;
}

.search-form .btn-custom {
position: absolute;
top: 0;
right: -5px;
width: 40px;
height: 100%;

background:linear-gradient(to right, #585d9100, #3A6796, #416193);
color: #fff;
}


body {
margin: 0;
padding: 0;
background: linear-gradient(to bottom, #585d9100, #3A6796, #416193);
}

section {
content: '';
background: linear-gradient(to top, black, transparent);
bottom: 0;
height: 25%;
width: 100%;
}

.router-link {
color: black;
}


/* 트랜지션 */
.fade-enter {
opacity: 0;
}

.fade-enter-active,
.fade-leave-active {
transition: opacity 0.5s ease-out;
}

.fade-leave-to {
opacity: 0;
}

.slide-fade-enter {
transform: translateX(10px);
opacity: 0;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
transition: all 0.2s ease;
}

.slide-fade-leave-to {
transform: translateX(-10px);
opacity: 0;
}

/* 모달부분 */
.modal {
position: fixed;
top: 0;
left: 0;
width: 100%;
height: 100%;
background-color: rgba(0, 0, 0, 0.5);
display: flex;
justify-content: center;
align-items: center;
z-index: 999;
}

.modal-content {
background-color: #fff;
padding: 20px;
border-radius: 8px;
}


/* 네비게이션바 */
@media (max-width: 992px) {
.nav-container {
display: none;
}

.main-container {
margin-top: 0;
}
}
</style>
