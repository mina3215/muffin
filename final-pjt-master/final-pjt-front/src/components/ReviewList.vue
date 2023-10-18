<template>
  <div @click="goToReviewDetail" class="comments d-flex">
    <div class="comment-content">
      
      <div  >
      {{ review.title }}
      </div>
    </div>
    <router-link 
      :to="{
        name: 'profile',
        params : {username: username}
      }" style="color: black; text-decoration: none;">
      <div class="comment-score">
          | 작성자: {{ username }}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          {{ date }}
      </div>
    </router-link>
  </div>
</template>

<script>
import axios from 'axios';
const API_URL = 'http://127.0.0.1:8000/muffins/';
export default {

  name: 'ReviewList',
  
  data(){
    return{
      username : null
    }
  },
  props: {
    review: Array,
  },
  components:{
  },
  methods: {
    
    goToReviewDetail() {
    this.$router.push({
      name: 'reviewboarddetail',
      params: {
        id : this.$route.params.id,
        reviewId: this.review.id
      }
    });
    
    },
    // goToReviewDetail() {
    //   this.$router.push(`/reviewboard/${this.movieId}/detail/${this.review.id}`);
    getUserName(){
      const author = this.review.author

      axios({
        method: 'get',
        url: `${API_URL}accounts/profile/${author}/`,
      })
      .then((res)=>{
        console.log(res.data)
        this.username = res.data.username
      })
      .catch((err)=>{
        console.log(err,'바보')
      })
    },

  },
  
  mounted(){
    this.movieId = this.$route.params.id; // 라우트 파라미터 할당
    this.getUserName()
  },
  computed:{
    date(){
    const review_created_at = this.review.created_at
    return review_created_at ? review_created_at.slice(0, 10) : ''
  }
  }
};
</script>

<style>
.comments {
  color: black;
  display: flex;
  font-weight: bold;
  margin-top: 4px;
  justify-content: space-between; 
}

.comment-score {
  margin-left: auto; 
}
</style>
