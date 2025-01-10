<template>
  <v-menu
    v-model="menuStatus"
    bottom
    min-width="130px"
    rounded
    offset-y
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        icon
        v-on="on"
        v-bind="attrs"
      >
        <v-avatar size="36" >
          <img
            :key="$store.state._avatar_url_"
            :src="$store.state._avatar_url_"
          >
        </v-avatar>
      </v-btn>
    </template>
    <v-card>
      <v-list-item>
        <v-list-item-content class="justify-center">
          <div class="mx-auto text-center">
            <v-row no-gutters>
              <v-col class="text-center">
                <v-btn depressed text @click="navigateTo('/follows')">
                  <div>
                    <h2> {{ $store.state._follows_ }} </h2>
                    关注
                  </div>
                </v-btn>
              </v-col>
              <v-col class="text-center">
                <v-btn depressed text @click="navigateTo('/favorites')">
                  <div>
                    <h2> {{ $store.state._favorites_ }} </h2>
                    收藏
                  </div>
                </v-btn>
              </v-col>
              <v-col class="text-center">
                <v-btn depressed text @click="navigateTo('/resources/own')">
                  <div>
                    <h2> {{ $store.state._shares_ }} </h2>
                    分享
                  </div>
                </v-btn>
              </v-col>
              <v-col class="text-center">
                <v-btn depressed text @click="navigateTo('/tasks/own')">
                  <div>
                    <h2> {{ $store.state._missions_ }} </h2>
                    任务
                  </div>
                </v-btn>
              </v-col>
            </v-row>
            <v-divider class="my-3" />
            <v-btn depressed rounded text @click="navigateTo('/resources/share')">
              分享资源
            </v-btn>
            <v-divider class="my-3" />
            <v-btn depressed rounded text @click="navigateTo('/tasks/add')">
              发布悬赏
            </v-btn>
            <v-divider class="my-3" />
            <v-btn depressed rounded text @click="navigateTo('/center')">
              个人中心
            </v-btn>
            <v-divider class="my-3" />
            <v-btn rounded text color="error" @click="logout">
              注销
            </v-btn>
          </div>
        </v-list-item-content>
      </v-list-item>
    </v-card>
  </v-menu>
</template>

<script>
export default {
  data() {
    return {
      menuStatus: false,
    };
  },
  watch: {
    menuStatus(newStatus) {
    if (newStatus) {
      this.updateInfo();
    }
  }
  },
  methods: {
    navigateTo(route) {
      this.$router.push(route).catch((err) => {
        if (err.name !== "NavigationDuplicated") {
          throw err;
        }
      });
    },
    logout() {
      this.$store.commit("clearPersonalInfo");
      this.$router.push("/auth");
    },
    updateInfo() {
      this.$store.dispatch("getFollows", { id: this.$store.state._user_id_ })
        .then((res) => {
          this.$store.commit("setFollows", res.total);
        })
        .catch((err) => {
          this.$store.commit("setAlert", {
            type: "error",
            message: err,
          });
        });
      this.$store.dispatch("ownPosts",)
        .then((res) => {
          this.$store.commit("setShares", res.total);
        })
        .catch((err) => {
          this.$store.commit("setAlert", {
            type: "error",
            message: err,
          });
        });
      this.$store.dispatch("getFavorites", { id: this.$store.state._user_id_ })
        .then((res) => {
          this.$store.commit("setFavorites", res.total);
        })
        .catch((err) => {
          this.$store.commit("setAlert", {
            type: "error",
            message: err,
          });
        });
      this.$store.dispatch("ownTasks")
        .then((res) => {
          this.$store.commit("setMissions", res.total);
        })
        .catch((err) => {
          this.$store.commit("setAlert", {
            type: "error",
            message: err,
          });
        });
    }
  },
};
</script>

<style scoped>
.v-card {
  backdrop-filter: blur(10px); /* 毛玻璃效果 */
  border-radius: 8px;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
  width: fit-content;
  min-width: 290px;
}

.v-list-item {
  width: 100%;
}

.v-btn {
  width: 100%;
  height: fit-content;
}
</style>