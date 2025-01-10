<template>
  <div>
    <Loading v-if="loading" />
    <v-container style="max-width: 70%;" v-else>
      <v-alert type="info" v-if="posts.length == 0">你还没有收藏任何资源哦。</v-alert>
      <div class="posts-list" v-else>
        <div v-for="(post, index) in posts" :key="index">
          <div :class="[$vuetify.theme.dark ? 'card-dark' : 'card-light']">
            <!-- Post Info Section -->
            <div @click="viewPost(post.id)" class="ma-0 pa-0">
              <h3>{{ post.title }}</h3>
              <v-chip v-for="(tag, tagIndex) in post.tags" :key="tagIndex" color="light-green" label small class="mt-3 tag">
                {{ tag }}
              </v-chip>
              <p class="info-text mt-3 pd-0">
                <span class="mx-3">
                  <v-icon>mdi-account</v-icon>
                  <a :href="`/center/${post.created_by.user_id}`" @click.stop class="ml-2" style="font-size: 16px;" target="blank">
                    {{post.created_by.username}}
                  </a>
                </span>
                <span> 分享时间: <span class="timestamp">{{ format(post.created_at, 'yyyy-MM-dd HH:mm:ss') }}</span> </span>
              </p>
            </div>
            <!-- Action Buttons on Top Right -->
            <div class="action-buttons">
              <v-btn icon @click="removeFavorite(post.id)" class="remove-btn">
                <v-icon>mdi-heart-remove</v-icon>
              </v-btn>
            </div>
          </div>
        </div>
      </div>
    </v-container>
  </div>
</template>
<script>
import Loading from '../Loading.vue';
import { format } from 'date-fns';
export default {
  data() {
    return {
      loading: true,
      posts: [],
    };
  },
  components: {
    Loading,
    format,
  },
  methods: {
    viewPost(postId) {
      window.open(`/resources/${postId}`, "_blank");
    },
    removeFavorite(postId) {
      this.$store.dispatch("notFavourPost", {id: postId})
        .then((res) => {
          this.$store.commit("setFavorites", this.$store.state._favorites_ - 1);
          this.posts = this.posts.filter((post) => post.id !== postId);
        })
        .catch((err) => {
          console.error(err);
        });
    },
    format,
  },
  mounted() {
    this.$store.commit("setAppTitle", "我的收藏");
    this.$store.dispatch("getFavorites", {id: this.$store.state._user_id_})
      .then((res) => {
        this.posts = res.favourites;
        this.loading = false;
      })
      .catch((err) => {
        console.error(err);
      });
  },
};
</script>

<style scoped>
.posts-list {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 10px;
}

.card-dark {
  display: flex;
  align-items: flex-start;
  padding: 20px;
  border-radius: 12px;
  background-color: rgb(23, 23, 28);
  margin-bottom: 15px;
  box-shadow: 0 8px 15px rgba(75, 75, 75, 0.1);
  position: relative;
  transition: all 0.3s ease;
}

.card-dark:hover {
  transform: translateY(-5px);
}

.card-light {
  display: flex;
  align-items: flex-start;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 15px;
  background-color: aliceblue;
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: all 0.3s ease;
}

.card-light:hover {
  transform: translateY(-5px);
}

.post-card {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.post-info {
  margin-left: 20px;
  color: #333;
}

.post-info h3 {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.info-text {
  font-size: 14px;
  color: #666;
}

.username {
  font-weight: 600;
  color: #3f51b5;
}

.timestamp {
  font-style: italic;
  color: #999;
}

.tag {
  background-color: #1ba160;
  color: #fff;
  border-radius: 15px;
  margin-right: 8px;
  margin-bottom: 0px;
}

.action-buttons {
  position: absolute;
  top: 15px;
  right: 15px;
  display: flex;
  gap: 12px;
}

.view-btn, .remove-btn {
  color: #3f51b5;
  transition: color 0.3s ease;
}

.view-btn:hover, .remove-btn:hover {
  color: #ff4081;
}

.view-btn, .remove-btn {
  font-size: 20px;
}

.view-btn v-icon, .remove-btn v-icon {
  font-size: 24px;
}
</style>
