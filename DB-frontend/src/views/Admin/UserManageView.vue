<template>
  <v-container fluid class="pa-6">
    <p class="text-h4 mt-6 mb-4">所有用户</p>
    <p class="text-subtitle-2 mb-4">封禁、解封用户</p>
    <v-data-table
    :headers="headers"
    :items="allUser"
    class="elevation-0"
    disable-sort sticky
    >
      <template v-slot:item.index="{ index }">
        {{ index + 1 }}
      </template>
      <template v-slot:item.avatarurl="{ item }">
        <v-avatar size="32">
          <img :src="item.avatar" alt="User Avatar" />
        </v-avatar>
      </template>

      <template v-slot:item.isblock="{ item }">
        <v-btn
          :outlined="true"
          small
          :color="item.isblock ? 'green' : 'red'"
          class="me-1"
          @click="dialog(item.isblock, item.username, item.id)"
        >
          <v-icon small>
            {{ item.isblock ? 'mdi-account-check' : 'mdi-account-off' }}
          </v-icon>
        </v-btn>
      </template>
    </v-data-table>
    <v-dialog max-width="500px" v-model="dialogActive">
      <v-card>
        <v-toolbar flat>
          <v-toolbar-title>{{ dialogType ? "解封" : "封禁" }}用户</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn icon @click="dialogActive = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
        <v-card-text>
          确定要{{ dialogType ? "解封" : "封禁" }}用户“{{ dialogUserName }}”？
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="dialogActive = false">取消</v-btn>
          <v-btn :color="dialogType ? 'green' : 'red'" :loading="submitLoading" @click="onBlockUnblockClick">
            {{ dialogType ? "解封" : "封禁" }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>
<script>
  import { mapMutations } from "vuex";
  export default {
  data() {
    return {
      headers: [
        { text: "ID", value: "index" },
        { text: "头像", value: "avatarurl" },
        { text: "用户名", value: "username" },
        { text: "电子邮件地址", value: "email" },
        { text: "操作", value: "isblock" },
      ],
      allUser: [],
      dialogActive: false,
      dialogType: false, // true 表示解封，false 表示封禁
      dialogUserName: "",
      dialogUserID: 0,
      submitLoading: false,
    };
  },
  methods: {
    ...mapMutations(["setAppTitle", "setAlert"]),
    // 获取所有用户数据
    getAllUser() {
      this.$store.dispatch("getAllUsers").then((res) => {
        this.allUser = res.users;
      })
      .catch((err) => {
        this.setAlert({
          type: "error",
          message: err,
        });
      });
    },
    // 打开确认对话框
    dialog(isUnblock, username, id) {
      this.dialogType = isUnblock;
      this.dialogUserName = username;
      this.dialogUserID = id;
      this.dialogActive = true;
    },
    // 提交封禁/解封操作
    onBlockUnblockClick() {
      this.submitLoading = true;
      if (this.dialogType) {
        // 解封用户
        this.$store.dispatch("unblockUser", {id: this.dialogUserID})
          .then(() => {
            this.setAlert({
              type: "success",
              message: `解封用户“${this.dialogUserName}”成功！`,
            });
            this.dialogActive = false;
            this.getAllUser(); // 更新用户列表
          })
          .catch((err) => {
            this.setAlert({
              type: "error",
              message: err,
            });
          });
      } else {
        // 封禁用户
        this.$store.dispatch("blockUser", {id: this.dialogUserID})
          .then(() => {
            this.setAlert({
              type: "success",
              message: `封禁用户“${this.dialogUserName}”成功！`,
            });
            this.dialogActive = false;
            this.getAllUser(); // 更新用户列表
          })
          .catch((err) => {
            this.setAlert({
              type: "error",
              message: err,
            });
          });
      }
      this.submitLoading = false;
    },
  },
  mounted() {
    this.setAppTitle("用户管理");
    this.getAllUser();
  },
};
</script>