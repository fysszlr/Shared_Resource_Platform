<template>
  <v-app>
    <partice v-if="$store.getters.hasParticles" />
    <v-app-bar app v-if="$store.state._show_platform_frame_" class="px-5">
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <img src="@/assets/images/logo.png" alt="our logo" class="logo" style="cursor: pointer;" @mouseover="showWelcome = true" @mouseleave="showWelcome = false">
      <v-toolbar-title v-if="showWelcome" style="margin-left: 20px;" class="welcome-text">航 U 邦欢迎您！</v-toolbar-title>
      <v-toolbar-title v-if="!showWelcome" style="margin-left: 20px;">{{ $store.state._app_title_ }}</v-toolbar-title>
      <v-spacer></v-spacer>
      <div class="pr-4">{{ getCurrentTimeGreetings() }}，{{ $store.state._user_name_ }}</div>
      <v-btn icon @click="toggleParticles" :color="$store.getters.hasParticles ? 'primary' : 'grey'">
        <v-icon>
          mdi-apache-kafka
        </v-icon>
      </v-btn>
      <v-btn icon @click="changeMode">
        <v-icon transition="scale-transition">
          {{ this.$vuetify.theme.dark ? 'mdi-weather-night' : 'mdi-white-balance-sunny' }}
        </v-icon>
      </v-btn>
      <avatar-menu />
    </v-app-bar>


    <v-navigation-drawer v-model="drawer" fixed temporary>
      <div class="d-flex flex-column" style="height: 100%;">
        <v-list class="flex-grow-1">
          <v-list-item v-for="[icon, text, route] in ($store.state._role_ == 'Administrator' ? admin_links : links)" :key="icon" link @click="navigateTo(route)">
            <v-list-item-icon>
              <v-icon>{{ icon }}</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>{{ text }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
        <v-spacer></v-spacer>
        <v-list>
          <v-list-item link @click="handleAboutClick" class="about-btn">
            <v-list-item-icon>
              <v-icon>mdi-progress-question</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>关于</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </div>
    </v-navigation-drawer>
    <v-main>
      <router-view />
    </v-main>
    <alert />
  </v-app>
</template>

<script>
import Partice from './components/Partice.vue';
import Alert from './components/Alert.vue';
import AvatarMenu from './components/AvatarMenu.vue';
export default {
  name: 'App',
  components: {
    Partice,
    Alert,
    AvatarMenu,
  },
  data() {
    return {
      showWelcome: false, // 控制欢迎文字的显示
      drawer: false,
      admin_links: [
        ['mdi-home', '首页', '/'],
        ['mdi-book-open-variant-outline', '共享资源站', '/resources'],
        ['mdi-account-group', '任务悬赏站', '/tasks'],
        ['mdi-account', '个人中心', '/center'],
        ['mdi-newspaper-variant-multiple-outline', '管理公告', '/admin/newsManage'],
        ['mdi-account-cog', '管理用户', '/admin/userManage'],
      ],
      links: [
        ['mdi-home', '首页', '/'],
        ['mdi-book-open-variant-outline', '共享资源站', '/resources'],
        ['mdi-account-group', '任务悬赏站', '/tasks'],
        ['mdi-account', '个人中心', '/center'],
      ]
    };
  },

  methods: {
    navigateTo(route) {
      this.$router.push(route).catch(err => {
        if (err.name !== 'NavigationDuplicated') {
          throw err;
        }
      });
    },
    handleAboutClick() {
      this.navigateTo('/about');
    },
    changeMode() {
      this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
      localStorage.setItem('__dark_theme__', this.$vuetify.theme.dark);
      this.$store.commit("setAlert", this.$vuetify.theme.dark ? { "type": "success", "message": "黑暗模式已启用。" } : { "type": "success", "message": "黑暗模式已关闭。" });
    },
    toggleParticles() {
      this.$store.commit("setParticles", !this.$store.getters.hasParticles);
      localStorage.setItem('__particles__', this.$store.getters.hasParticles);
      this.$store.commit("setAlert", this.$store.getters.hasParticles ? { "type": "success", "message": "背景颗粒已启用。" } : { "type": "success", "message": "背景颗粒已关闭。" });
    },
    getCurrentTimeGreetings() {
        const h = new Date().getHours()
        if (h < 2) return '夜深了'
        if (h < 6) return '别卷了'
        if (h < 12) return '上午好'
        if (h < 13) return '中午好'
        if (h < 18) return '下午好'
        if (h < 23) return '晚上好'
        return '夜深了'
      },
  },
  created() {
    if (localStorage.getItem('__token__') && localStorage.getItem('__user_name__')) {
      this.$store.commit('setAlert', {
        type: "success",
        message: "别来无恙，" + localStorage.getItem('__user_name__') + "。",
      });
    }
  },
  beforeCreate() {
    if (localStorage.getItem('__dark_theme__')) {
      this.$vuetify.theme.dark = localStorage.getItem('__dark_theme__') === 'true';
    } else {
      this.$vuetify.theme.dark = false;
    }
    if (localStorage.getItem('__particles__')) {
      this.$store.commit("setParticles", localStorage.getItem('__particles__') === 'true');
    } else {
      this.$store.commit("setParticles", true);
    }
  }
};
</script>


<style lang="scss">
  @import './assets/styles/main.scss';

  #particles-js {
    width: 100%;
    height: calc(100vh - 64px);
    position: absolute;
  }

  .slide-y-enter-active,
  .slide-y-leave-active {
    transition: all 0.5s ease;
  }

  .slide-y-enter,
  .slide-y-leave-to {
    transform: translateY(100%);
    opacity: 0;
  }

  .scale-transition {
    transition: transform 0.3s ease;
  }
  .scale-transition-enter-active {
    transform: scale(1.2);
  }
  .scale-transition-leave-active {
    transform: scale(0.8);
  }
  .logo {
    vertical-align: middle;
    margin-left: 0px;
    margin-top: 0px;
    width: 65px;
    height: auto;
  }
  .welcome-text {
    background-color: rgba(249, 234, 134, 0.9); /* 使用明亮的黄色背景 */
    color: #ed5e5e; /* 使用红色文字 */
    padding: 8px 15px; /* 增加内边距 */
    border-radius: 10px; /* 增加圆角 */
    white-space: nowrap; /* 不换行 */
    transition: opacity 0.3s; /* 过渡效果 */
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4); /* 添加阴影效果 */
    font-weight: bold; /* 加粗字体 */
    font-size: 16px; /* 调整字体大小 */
  }
</style>