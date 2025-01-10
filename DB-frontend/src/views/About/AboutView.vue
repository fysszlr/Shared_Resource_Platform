<template>
  <v-container style="margin-top:45px">
    <v-card class="mb-10">
      <v-card-title>
        <h2 style="font-size: 24px;" @click="showImage = true">
          关于平台
          <img src="@/assets/images/logo.png" alt="our logo" class="welcome-image" style="cursor: pointer;">
        </h2>
      </v-card-title>
      <v-divider class="my-0"></v-divider>
      <v-card-text>
        <div style="font-weight: bold; font-size: 18px;">
          这是 航U邦，一个用于分享资源和获取资源的平台。
        </div>
        <div style="font-size: 16px; margin-top:8px;">
          随着互联网的发展，学生和教师对在线学习资源的需求日益增长。然而，现有的一些平台并未完全满足学习者多样化的需求，尤其是在资料共享、悬赏任务等方面。因此，建立一个专门的学习资料分享网站，不仅可以弥补这些不足，还能为学生提供一个高效、灵活的学习环境。
        </div>
      </v-card-text>
    </v-card>
    <v-card>
      <v-card-title>
        <h2 style="font-size: 24px;">
          关于项目
          <router-link to="/giveMeMoney">
            <img src="@/assets/images/blogDefault.png" alt="our logo" class="welcome-image2" style="cursor: pointer;">
          </router-link>
          <!-- <img src="@/assets/images/blogDefault.png" alt="our logo" class="welcome-image2" style="cursor: pointer;"> -->
        </h2>
      </v-card-title>
      <v-divider class="my-0"></v-divider>
      <v-card-text>
        <div style="font-size: 16px;">
          这是一个基于 Vue2 和 Django 的开源项目。
          <br />
          项目代码托管于 <a href="https://github.com/zhangyitonggg/DB-frontend">GitHub</a>。
          <br />
          你所看到的页面渲染于 {{ new Date().toLocaleString() }}。
        </div>
        <br />
        <div style="font-size: 16px;">
          我们会不定期推出更新的版本来提升你的使用体验。如果你刷新页面后发现内容发生了变化，说明你的浏览器可能正在使用缓存内容渲染。
          <br />
          通常来说，缓存会在一段时间后自动更新。如果需要，请手动清理浏览器的缓存。
        </div>
        <br />
        <div style="font-size: 16px;">
          本项目的诞生离不开包括 Vue 和 Node.js 在内的众多开源项目。
        </div>
        <br>
        <v-divider class="my-0"></v-divider>  
        <div style="font-size: 16px;">
          感谢所有人对该项目提供的帮助。以下是项目的主要贡献者：
        </div>
        <br />
        <v-row>
          <v-col v-for="contributor in contributors" :key="contributor.id">
            <v-avatar size="50" :color="contributor.site_admin ? 'red' : 'blue'">
              <img :src="contributor.avatar_url" />
            </v-avatar>
            <h4 style="font-size: 16px;">
              <a :href="contributor.html_url">{{ contributor.login }}</a>
            </h4>
            <p style="font-size: 14px;">贡献次数：{{ contributor.contributions }}</p>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
          <!-- Modal for image -->
          <v-dialog v-model="showImage" max-width="500px">
            <v-card>
              <v-card-title class="headline">zyt 由衷地感谢您的指导！</v-card-title>
              <v-card-text>
                <v-img src="@/assets/images/thanks.png" alt="谢谢你" />
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn text @click="showImage = false">关闭</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
  </v-container>
</template>

<script>
export default {
name: 'AboutView',
data() {
  return {
    loading: false,
    showImage: false,  // 用于控制图片模态框的显示
    contributors: [
      {
        "login": "AOSTL",
        "id": 60469446,
        "node_id": "MDQ6VXNlcjYwNDY5NDQ2",
        "avatar_url": "https://avatars.githubusercontent.com/u/60469446?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/AOSTL",
        "html_url": "https://github.com/AOSTL",
        "followers_url": "https://api.github.com/users/AOSTL/followers",
        "following_url": "https://api.github.com/users/AOSTL/following{/other_user}",
        "gists_url": "https://api.github.com/users/AOSTL/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/AOSTL/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/AOSTL/subscriptions",
        "organizations_url": "https://api.github.com/users/AOSTL/orgs",
        "repos_url": "https://api.github.com/users/AOSTL/repos",
        "events_url": "https://api.github.com/users/AOSTL/events{/privacy}",
        "received_events_url": "https://api.github.com/users/AOSTL/received_events",
        "type": "User",
        "site_admin": false,
        "contributions": 38
      },
      {
        "login": "fysszlr",
        "id": 60469446,
        "node_id": "MDQ6VXNlcjYwNDY5NDQ2",
        "avatar_url": "https://avatars.githubusercontent.com/u/60098978?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/AOSTL",
        "html_url": "https://github.com/fysszlr",
        "followers_url": "https://api.github.com/users/AOSTL/followers",
        "following_url": "https://api.github.com/users/AOSTL/following{/other_user}",
        "gists_url": "https://api.github.com/users/AOSTL/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/AOSTL/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/AOSTL/subscriptions",
        "organizations_url": "https://api.github.com/users/AOSTL/orgs",
        "repos_url": "https://api.github.com/users/AOSTL/repos",
        "events_url": "https://api.github.com/users/AOSTL/events{/privacy}",
        "received_events_url": "https://api.github.com/users/AOSTL/received_events",
        "type": "User",
        "site_admin": false,
        "contributions": 46
      },
      {
        "login": "zhangyitongg",
        "id": 36978310,
        "node_id": "MDQ6VXNlcjM2OTc4MzEw",
        "avatar_url": "https://avatars.githubusercontent.com/u/144459286?s=400&u=75718067ed31c560cce4a58ae82a00f68065b193&v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/jhdonghj",
        "html_url": "https://github.com/zhangyitonggg",
        "followers_url": "https://github.com/zhangyitonggg",
        "following_url": "https://api.github.com/users/jhdonghj/following{/other_user}",
        "gists_url": "https://api.github.com/users/jhdonghj/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/jhdonghj/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/jhdonghj/subscriptions",
        "organizations_url": "https://api.github.com/users/jhdonghj/orgs",
        "repos_url": "https://api.github.com/users/jhdonghj/repos",
        "events_url": "https://api.github.com/users/jhdonghj/events{/privacy}",
        "received_events_url": "https://api.github.com/users/jhdonghj/received_events",
        "type": "User",
        "site_admin": false,
        "contributions": 37
      }
    ],
  };
},
mounted() {
  this.$store.commit('setAppTitle', '关于我们');
  this.$store.commit("setAlert", {
    type: "success",
    message: "欢迎来到关于我们页面！图标均可点击查看更多信息！  ",
  });
},
};
</script>

<style scoped>
.welcome-image {
  vertical-align: middle; 
  margin-left: -1px;
  margin-top: -3px;
  width: 65px;
  height: auto;
}
.welcome-image2 {
  vertical-align: middle; 
  margin-left: 8px;
  margin-top: -3px;
  width: 42px;
  height: auto;
}
</style>
