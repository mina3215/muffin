<template>
  <div class="box">
    <div class="container">
      <div class="row">
        <div class="info row-4">
          <!-- 영화 포스터(poster_path), 제목(title), 줄거리(overview)를 표시 -->
          <div v-if="movie" class="col text-center">
            <div class="image" @mouseover="showVideoOnDelay" @mouseleave="clearShowVideoTimeout; showVideo = false">
              <img :src="getFullImageUrl(movie.poster_path)" class="card-img-top img-fluid" alt="..." />
              <iframe v-if="showVideo" width="100%" height="100%" :src="getYoutubeUrl(movie.video_path)" frameborder="0" allowfullscreen loop></iframe>
              </div>
            <h1 class="p-3 mt-3 mb-3">{{ movie.title }}
              <span class="heart" @click="like_this_movie" v-if="movie">{{ movie.is_like ? "♥" : "♡" }}</span>
            </h1>
            <p class="lead">{{ movie.overview }}</p>
          </div>
          <p v-else class="text-center">Loading...</p>
        </div>
      </div>
      <hr>
      <h3>출연진</h3>
      <div class=" d-flex flex-row">
        <div v-for="actor in actors" :key="actor.id" class="router" style=" margin-right: 10px;">
          <router-link style="text-decoration: none; color: black;"
          
          :to="{
            name: 'actordetail',
            params: { 
              id: actor.id,
            },}" >
          <img :src="getFullImageUrl(actor.profile_path)" alt="..." style="width: 150px; height: 200px;" class="card-img-top img-fluid" />
          <p class="mt-3">{{actor.name}}</p>
          </router-link>

        </div>
      </div>
      <hr>
      <!-- 한 줄 감상평 섹션: 최대 5개의 한 줄 감상평을 표시.
      OneLineComment 컴포넌트를 사용하여 각 댓글을 표시 -->
      <div class="row-8 d-flex">
        <div class="col-12">
          <div class="my-5">
            <div v-if="comments.length > 0" class="text-left">
              <h3 class="mb-3">한 줄 감상평</h3>
              <div class="card mb-3" v-for="(comment, index) in comments" :key="comment.id" v-show="index < 5">
                <div class="card-body">
                  <OneLineComment :comment="comment" />
                </div>
              </div>
              <p v-if="comments.length > 5" class="text-center">
                ...
              </p>
            </div>
            <div v-else class="text-center">
              <p>작성된 한 줄 감상평이 없습니다.</p>
            </div>
          </div>
          <hr>
          <!-- 한 줄 감상평 작성하기 폼: 별점과 내용을 입력하여 한 줄 감상평을 작성할 수 있는 폼입니다. 폼을 제출하면 createOneline 메소드가 호출되어 감상평을 생성 -->
          <form class="my-4 p-5" @submit.prevent="createOneline">
            <div class="form-group">
              <label for="score"><h2> 별점</h2></label>
              <star-score v-model="score" :value="score" />
            </div>
            <br>
            <div class="form-group">
              <br class="p-3">
              <label for="content"><h3> 나도 한마디!</h3></label>
              <textarea id="content" class="form-control no-resize" rows="1" v-model="content"></textarea>
            </div>
            <br>
            <button type="submit" class="btn btn-primary btn-lg btn-block">등록하기</button>
          </form>
        </div>
        <!-- 리뷰 보드로 이동 -->
        
      </div>
      <div class="text-center">
          <transition name="fade">
            <button @click="goToReviewBoard" class="btn btn-secondary">리뷰 게시판으로 이동</button>
          </transition>
        </div>
    </div>
    
  <div class="modal" v-if="showModal">
    <div class="modal-content">
      <p class="modalhead">{{modal_title}} </p>
      <img :src="get_prize_img(modal_id)" alt="">
      <p>{{modal_Content}}</p>
      <button class="btn btn-outline-success" @click="hideModal ">닫기</button>




    </div>
    </div>
  </div>
  
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
import OneLineComment from '@/components/OneLineComment'
import StarScore from '@/components/StarScore'

const API_URL = 'http://127.0.0.1:8000/muffins/'

export default {
  name: 'MovieDetailView',
  components: {
    OneLineComment,
    StarScore,
  },
  data() {
    return {
      movie: null,
      content: '',
      score: '',
      author: '',
      showModal: false,
      modal_title : '',
      modal_Content : '', 
      showVideo: false,
      showVideoTimeout: null,
      modal_id : ''
    };
  },
  created() {
    this.loadMovieData();
  },
  methods: {
    goToReviewBoard() {
      this.$store.state.reviews.boardmovie_info['title'] = this.movie.title
      this.$store.state.reviews.boardmovie_info['img_path'] = this.movie.poster_path
      this.$router.push(`/reviewboard/${this.$route.params.id}`);

    },

    loadMovieData() {
      const movieId = this.$route.params.id;
      const storedMovieData = localStorage.getItem(`movie_${movieId}`);

      if (storedMovieData) {
        this.movie = JSON.parse(storedMovieData);
        this.getMovieComments();
      } else {
        this.getMovieDetail();
        this.getMovieComments();
      }
    },
    // 영화 디테일 가져옴.
    getMovieDetail(){
      const movieId = this.$route.params.id
      const username = this.$store.state.myAccounts.username
      console.log(this.$store.state.myAccounts.token)
      axios({
        headers: {
          Authorization: `Token ${this.$store.state.myAccounts.token}` // 로그인한 사용자의 토큰을 전송합니다.
        },
        method: 'get',
        url: `${API_URL}detail/${movieId}/${username}/`,

      })
      .then((res)=>{
        console.log(res.data)
        this.actors = res.data['actors']
        this.movie = res.data['movies']
      })
      .catch((err)=>{
        console.log(err,'바보')
      })
    },
    getMovieComments() {
      const movieId = this.$route.params.id;

      if (movieId) {
        axios({
          method: 'get',
          url: `${API_URL}comments/${movieId}/`,
        })
          .then((res) => {
            this.$store.commit('GET_COMMENTS', res.data);
          })
          .catch(() => {
            this.$store.state.comments = [];
          });
      }
    },
    createOneline() {
      const content = this.content.trim();
      const score = parseInt(this.score);

      if (!content) {
        alert('내용을 입력해주세요.');
        return;
      }

      if (!score) {
        alert('별점을 선택해주세요.');
        return;
      }

      const movieId = parseInt(this.$route.params.id)
      const author = this.$store.state.myAccounts.username;
      console.log(author)
      console.log("wowoowowowow")

      const data = {
        score,
        content,
        movie: movieId,
        author : author, 
      };

      axios
      .post(`${API_URL}comments/${movieId}/create/`, data, {
          headers: {
            Authorization: `Token ${this.$store.state.myAccounts.token}`
          }
        })
        .then(() => {
          this.content = '';
          this.score = null;
          this.getMovieComments();
        })
        .catch((err) => {
          console.log(err);
        });
    },
    getFullImageUrl(path) {
      if (path) {
        return `https://image.tmdb.org/t/p/original${path}`;
      }
      return ""; // 이미지 URL이 없는 경우 빈 문자열 반환
    },  
    getYoutubeUrl(path){
      if(path){
        return `https://www.youtube.com/embed/${path}?autoplay=1&mute=1`
      }
      return ""
    },

    //좋아요 상태 변경 ! 
    like_this_movie(){
      const user = this.$store.state.myAccounts.username
      const movieId = this.$route.params.id;
      axios({
        method: 'post',
        url: `${API_URL}like/${movieId}/`,
        data:{ "user" : user },
      })
      .then((res) => {
        console.log(!this.$store.state.myAccounts.prizes)
        if(res.data.is_like && !this.$store.state.myAccounts.prizes[2]){
          this.$store.state.myAccounts.prizes[2] = true
          this.modal_id = 2
          this.checkAchievement('인생 첫 영화','영화...좋아하세요?')
        }
        console.log(res)
        this.movie.is_like = res.data.is_like
        // this.userinfo.follower_cnt = res.data.follower_cnt
      })
      .catch((error)=>{
        console.log(error)
      })
    },
    checkAchievement(title, content) {
      this.modal_title = title
      this.modal_Content = content
      this.showModal = true
    },

    hideModal() {
      this.showModal = false;
    },
  
    showVideoOnDelay() {
      this.showVideoTimeout = setTimeout(() => {
        this.showVideo = true;
      }, 1500);
    },
    clearShowVideoTimeout() {
      clearTimeout(this.showVideoTimeout);
      this.showVideoTimeout = null;
    },
    get_prize_img(id){
    return require(`@/assets/prize${id}.png`)
    }  ,

  },
  computed: {
    ...mapState(['movies']),
    comments() {
      return this.$store.state.comments.slice().reverse();
    },
    movies() {
      return this.$store.state.movies
    },
  },
};
</script>

<style scoped>
.box{
    background: white;
    color: black;

  
    padding: 3rem; /* 패딩 값을 조정하여 이미지가 잘리지 않도록 설정 */

}
.router{
  text-decoration: none; /* 하이퍼링크의 밑줄을 제거합니다. */

}
.card {
  border: none;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-secondary {
  background-color: #6c757d;
  border-color: #6c757d;
}

.form-select {
  width: 100%;
  height: 2.5rem;
}

.text-center {
  text-align: center;
}



.image {
  position: relative;
  width: 100%;
  padding-top: 100%;
  overflow: hidden;
  z-index: 2; /* 이미지가 동영상 위에 표시되도록 설정 */
}

.image img {
  position: absolute;
  top: 0;
  left: 0;
  /* width: 100%;
  height: 100%; */
  object-fit: cover;
}
.image::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%; /* Adjust the height of the transparent gradient */
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0), rgba(255, 255, 255, 100));
  z-index: 2;
}
iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1; /* 동영상이 이미지 위에 표시되도록 설정 */
}
.image:hover::before {
  opacity: 0; /* Make the gradient overlay disappear on hover */
}

/* 리사이즈 금지 */
.no-resize {
  resize: none;
}

.heart {
  font-size: 2rem; /* Adjust the desired font size */
  -webkit-text-fill-color: red;
  -webkit-text-stroke-width: 2.3px;
  -webkit-text-stroke-color: #ff4489c2;
  cursor: pointer;
  -ms-user-select: none; 
  -moz-user-select: -moz-none;
  -khtml-user-select: none;
  -webkit-user-select: none;
  user-select: none;
}
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
font-weight: bold;
width: 550px;
height: 550px;
margin: auto;
padding: 20px;
font-size: 26px;

border-radius: 8px;
color: rgb(255, 255, 255);
  text-shadow: 0px 4px 9px black;
}
.modal-content .modalhead {
  font-size: 38px;
}
.modal-content p{
color: rgb(27, 25, 25);
text-shadow: 0px 4px 9px rgb(116, 116, 116);
}
.modal-content img{
  align-items: center;
  margin: auto;

  width: 70%;
  height: 70%;
}


</style>
