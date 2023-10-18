<template>
  <div class="ReviewForm">
    <form @submit.prevent="createReview" style="background-color: white;" class="p-5">
      <div class="">
        <input type="title" class="form-control p-3" id="TitleInput" rows="6" placeholder="제목" v-model="title" style="font-size: 60px; border: none;">
      </div>
      <hr>
      <div class="p-3">
        <label for="ContentInput" class="form-label"></label>
        <textarea class="form-control no-resize" id="ContentInput" placeholder="본문을 입력하세요." rows="50" v-model="content"></textarea>
      </div>
      <input type="submit" id="submit" value="작성완료" class="btn btn-primary mx-3">
      <button @click="goToReviewBoard" class="btn btn-primary">나가기</button>      

    </form>
  </div>
    


</template>

<script>
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/muffins/'

export default {
  name : 'ReviewForm',
  data(){
    return {
      title : '',
      content : '',      
      author : '',
    };
  },
  methods:{
    // 리뷰 게시글 생성
    createReview(){
      const title = this.title
      const content = this.content
      const movieId = this.$route.params.id
      const author = this.$store.state.myAccounts.username

      if(!title){
        alert('제목을 입력하세요.')
      }else if(!content){
        alert('내용을 입력하세요.')
      }

      const data = {
      title,
      content,
      movie: movieId,
      author : author, 
       };

      axios
      .post(`${API_URL}movies/${movieId}/reviews/`, data, {
          headers: {
            Authorization: `Token ${this.$store.state.myAccounts.token}`
          }
        })
        .then(() => {
          this.goToReviewBoard()
        })
        .catch((err) => {
          console.log(err)
        })
    },
      // 리뷰 게시판으로 이동
      goToReviewBoard(){
        this.$router.push(`/reviewboard/${this.$route.params.id}`)
    },
  },

}
</script>
