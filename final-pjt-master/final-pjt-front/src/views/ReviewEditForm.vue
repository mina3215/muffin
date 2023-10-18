<template>
  <!-- <div>
    {{filteredReview}}
    dddd
  </div> -->
  <div class="ReviewForm">
    <form @submit.prevent="editReview" style="background-color: white;" class="p-5">
      <div class="">
        <input type="title" class="form-control p-3" id="TitleInput" rows="6" placeholder="제목" v-model="filteredReview.title" style="font-size: 60px; border: none;">
      </div>
      <hr>
      <div class="p-3">
        <label for="ContentInput" class="form-label"></label>
        <textarea class="form-control no-resize" id="ContentInput" placeholder="본문을 입력하세요." rows="50" v-model="filteredReview.content"></textarea>
      </div>
      <input type="submit" id="submit" value ="수정" class="btn btn-secondary">
      <button @click="goToReviewDetail" class="btn btn-secondary">나가기</button>      

    </form>
  </div>
</template>
  
<script>
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/muffins/'

export default {
  name: 'ReviewEditForm',
  data() {
    return {
      title: '',
      content: '',
      author: '',
      reviewId: null,
      Article_username : ''
    };
  },
  mounted() {
    this.reviewId = this.$route.params.reviewId;
    this.getUserName() 
  },
  methods: {
    // 리뷰 게시글 수정
    editReview() {
      const title = this.filteredReview.title
      const content = this.filteredReview.content
      const movieId = this.$route.params.id;
      const author = this.filteredReview.author
      const reviewId = this.reviewId

      if (!title) {
        alert('제목을 입력하세요.')
      } else if (!content) {
        alert('내용을 입력하세요.')
      }

      const data = {
        title : title,
        content : content,
        movie: movieId,
        author: author,
        id: reviewId
      };
      console.log(data)
      axios
        .put(`${API_URL}movies/${movieId}/reviews/${reviewId}/`, data, {
          headers: {
            Authorization: `Token ${this.$store.state.myAccounts.token}`
          }
        })
        .then(() => {
          this.goToReviewDetail()
        })
        .catch((err) => {
          console.log(err);
        })
    },


    //리뷰 디테일 뷰로 돌아가기
    goToReviewDetail(){
          this.$router.push(`/reviewboard/${this.$route.params.id}/detail/${this.$route.params.reviewId}/`)
    },

    
    //유저네임 변환
    getUserName() {
      const author = this.filteredReview.author

      axios({
        method: 'get',
        url: `${API_URL}accounts/profile/${author}/`,
      })
        .then((res) => {
          console.log(res.data)
          this.Article_username = res.data.username
        })
        .catch((err) => {
          console.log(err, '바보')
        })
    },
  },

  computed: {
    filteredReview() {
      const targetReviewId = this.reviewId
      const movieReviews = this.$store.state.reviews.movie_reviews

      // 일치하는 리뷰만 필터링하여 반환
      return movieReviews.filter(review => review.id == targetReviewId)[0]
    }
  },



}
</script>

<style>
.no-resize {
  resize: none;
}

hr {
  border-top: 1px solid #00000079;
}
</style>
  