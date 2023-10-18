<template>
  <div>
    <h1 class="p-3">{{this.$store.state.reviews.boardmovie_info['title']}} 게시판</h1>
    <hr>
   
    
    <div class="card " v-for="review in reviews" :key="review.id">
      <div class="card-body">
        <review-list :review="review" />
      </div>
    </div>
    
    <div class=" p-5">
    <button @click="goToReviewForm" class="btn btn-primary mx-3">
      작성하기
    </button>
    <button @click="goToMovieDetail" class="btn btn-primary mx-3">
      돌아가기
    </button>
  </div>
  </div>
</template>


<script>
import ReviewList from '@/components/ReviewList';

export default {
  name: 'ReviewBoard',
  components: {
    ReviewList
  },
  data() {
    return {
      movieId: null, // movieId 변수 추가
    };
  },
  methods: {
    // 리뷰 작성폼으로 이동
    goToMovieDetail(){
      this.$router.push(`/moviedetail/${this.movieId}/`);
    },
    goToReviewForm() {
      this.$router.push(`/reviewboard/${this.movieId}/form/`);
    },
    // 리뷰 불러오기
    getReviews() {
      const movieId = this.movieId;
      this.$store.dispatch('reviews/getReviews', movieId);
    },
    goToReviewBoard(){
          this.$router.push(`/reviewboard/${this.$route.params.id}`);
      },
  },
  mounted() {
    this.movieId = this.$route.params.id; // 라우트 파라미터 할당
    this.getReviews(); // 리뷰 불러오기 메소드 호출
  },
  computed: {
    reviews() {
      return this.$store.state.reviews.movie_reviews.slice().reverse();
    },

    movie_name(){
      const movie = this.$store.state.movies
      const targetmovieId = this.$route.params.id
      return movie.filter(movie => movie.id == targetmovieId)[0];
    }
  },
};
</script>


<style scoped>
.card-body {
  word-wrap: break-word;
}
hr{
border: 0;
height: 1px;
background: #333;
background-image: -webkit-linear-gradient(left, #ccc, #333, #ccc); 
background-image:    -moz-linear-gradient(left, #ccc, #333, #ccc); 
background-image:     -ms-linear-gradient(left, #ccc, #333, #ccc); 
background-image:      -o-linear-gradient(left, #ccc, #333, #ccc); 
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
</style>