<template>
  <div class="actorboard">
    <header class="py-5 bg-image-full" style="background-color: rgba(19, 19, 54, 0.408); position: relative;">
      <div class="option_area">
        <div class="actor-wrapper">
          <!-- 이스터 에그 발동! -->
          <div v-if="id == 314159265359">
            <img src="@/assets/ye.png" class="rounded-image" alt="">            
          </div>
          <div v-else>
            <img :src="getFullImageUrl(actor.profile_path)" class="rounded-image" alt="..." />
          </div>  

          <div class="actor-name"><h1>{{ actor.name }}</h1></div>
          <div>{{ actor.fan_cnt }}명이 응원하고 있어요!</div>
        </div>
        <div class="icon-container">
          <h1 class="heart-icon" @click="follow()">{{actor.is_follow?'♥':'♡'}}</h1>
        </div>
      </div>
    </header>
    <main>
      <h2 style="text-align: left; margin-left: 20px; margin-top:20px ">
        출연작
      </h2>
      <div>
        <div style="display: flex; flex-wrap: nowrap; position: relative;">
          <div v-for="movie in movies" :key="movie.id" style="flex: 0 0 auto; margin-right: 10px;">
            <router-link
              :to="{
                name: 'moviedetail',
                params: { id: movie.id },
              }">
              <img :src="getFullImageUrl(movie.poster_path)" style="width: 150px; height: 200px; margin-left: 10px;" class="card-img-top img-fluid" alt="..." />
            </router-link>
          </div>
        </div>
      </div>
      <br><br>
      <h3 class="mb-3">응원 메시지</h3>
      <form class="my-4 p-5" @submit.prevent="createOneline">
        <div class="form-group">
          <label for="content"> <h4>나도 한마디!</h4> </label>
          <textarea class="form-control no-resize" rows="1" v-model="content"></textarea>
        </div>
        <br>
        <button type="submit" class="btn btn-primary btn-lg btn-block">등록하기</button>
      </form>
      <div class="row-8 d-flex">
        <div class="col-12">
          <div class="my-5">
            <div v-if="comments&&comments.length > 0" class="comments-container" >
              <div class="card mb-3" v-for="(comment, index) in comments.slice().reverse()" :key="comment.id" v-show="index < 3">
                <div class="card-body mb-3">
                  <OneLineComment :comment="comment" />
                </div>
              </div>
              <p v-if="comments.length > 3">
                ...
              </p>
              </div>
            <div v-else>
              <p>작성된 한 줄 감상평이 없습니다.</p>
            </div>
          </div>
        </div>
      </div>

        <div v-if="showModal">
          <div class="modal">
           <div class="modal-content">
            <p class="modalhead">{{modal_title}} </p>
            <img :src="get_prize_img(modal_id)" alt="">
            <p>{{modal_Content}}</p>
            <button class="btn btn-outline-success" @click="hideModal ">닫기</button>
          </div>
        </div>
      </div>

    </main>
    
</div>
  
</template>

<script>
import axios from 'axios'
import OneLineComment from '@/components/OneLineComment'
const API_URL = 'http://127.0.0.1:8000/muffins/'

export default {
  name:'ActorBoard',
  components : {
    OneLineComment
  },
  data(){
    return{
      showModal: false, 
      movies : null,
      actor : null,
      content: '',
      author: '',
      comments : null,

      modal_title : '',
      modal_Content : '',
      modal_id: '',
    }
  },
  computed : {
    get_profile_path(){
      return this.actor.profile_path
    }
  },
  props: {
    id: Number
  },
  created(){
    this.get_movies_of_actor()
  },
  methods:{
    getFullImageUrl(path) {
      if (path) {
        return `https://image.tmdb.org/t/p/original${path}`;
      }
      return ""; // 이미지 URL이 없는 경우 빈 문자열 반환
    },
    get_movies_of_actor(){
      const username = this.$store.state.myAccounts.username
      console.log(typeof(this.id))
      axios({
        method: 'get',
        url: `${API_URL}fan_community/detail/${this.id}/${username}/`,
      })
      .then((res) => {
        console.log(res.data['actor'])
        this.movies = res.data['movies']
        this.actor = res.data['actor']
        this.getActorComments()
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
    follow(){
      const username = this.$store.state.myAccounts.username
      axios({
        method: 'post',
        url: `${API_URL}fan_community/follow/${this.actor.id}`,
        data:{ "username" : username },
      })
      .then((res) => {
        // console.log(this.actor.id, res.data.is_follow, !this.$store.state.myAccounts.prizes[3] )
        if(this.actor.id === 314159265359 && res.data.is_follow && !this.$store.state.myAccounts.prizes[3]){
          this.$store.state.myAccounts.prizes[3] = true
          if(!this.$store.state.myAccounts.prizes[1]){
            this.$store.state.myAccounts.prizes[1] = true
          }
          this.modal_id = 3
          this.checkAchievement('앗! 이럴수가 이곳은 이제 매드 사이언티스트가 장악했습니다?','후후훗, 이 사이트는 너무 쉽네요')
        }
        else if(!this.$store.state.myAccounts.prizes[1] && res.data.is_follow){
          this.$store.state.myAccounts.prizes[1] = true
          this.modal_id = 1
          this.checkAchievement('입덕','난생 처음으로 배우를 팔로우 하셨군요!')
        }
        this.actor.is_follow = res.data.is_follow
        this.actor.fan_cnt = res.data.fan_cnt
      })
      .catch((error)=>{
        console.log(error)
      })
    },
    createOneline() {
      const content = this.content.trim();

      if (!content) {
        alert('내용을 입력해주세요.');
        return;
      }
      const author = this.$store.state.myAccounts.username;
      const data = {
        content,
        author : author, 
      }
      axios({
        method: 'post',
        url: `${API_URL}fan_community/createcomments/${this.actor.id}/`,
        data: data
      })
      .then((res) => {
        if(res.data.get_first_4 && !this.$store.state.myAccounts.prizes[4])
        {
          this.$store.state.myAccounts.prizes[4] = true
          this.checkAchievement('찐팬','같은 배우를 10번 응원했어요!')
          this.modal_id = 4
        }
        this.content = '';
        this.getActorComments();
      })
      .catch((err) => {
        console.log(err);
      });
    },
    getActorComments() {
      const actorId = this.id;
      if (actorId) {
        axios({
          method: 'get',
          url: `${API_URL}fan_community/createcomments/${actorId}/`,
        })
        .then((res) => {
          this.comments = res.data
        })
        .catch(() => {
          this.$store.state.comments = [];
        });
      }
    },
    get_prize_img(id){
    return require(`@/assets/prize${id}.png`)
    }  ,
 
    hideModal() {
        this.showModal = false
    },


  }
}
</script>


<style scoped>
.actorboard{
  font-size: 20px;
  
  color: white;


}
h1{
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 20px;
  color: white;
  text-shadow: 0px 4px 9px black;
}
h2{
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 20px;
  color: white;
  text-shadow: 0px 4px 9px black;
}
h3{
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 20px;
  color: white;
  text-shadow: 0px 4px 9px black;
}
.rounded-image {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  object-fit: cover;
  object-position: center;
  clip-path: ellipse(50% 50% at 50% 50%);
}
.actor-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.actor-name {
  margin-top: 10px;
  text-align: center;
}
.card {
  border: none;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1rem rgba(61, 49, 100, 0.15);
}
.heart-icon {
  color: white;
  cursor: pointer;
}
.icon-container {
  position: absolute;
  top: 30px;
  right: 40px;
}
.comments {
  color: black;
  display: flex;
  justify-content: space-between; /* 내용과 별점을 좌우로 분리 */
}

.comment-score {
  margin-left: auto; /* 별점을 오른쪽으로 이동 */
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
