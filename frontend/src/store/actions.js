import api from "../api";

export default {
  async login(context, { username, password, remember }) {
    return await api.login(username, password)
      .then(async response => {
        return await api.getUserProfile(response.user_id)
          .then((profile) => {
            let avatar = profile.avatarurl;
            localStorage.setItem('_user_avatar_', avatar);
            localStorage.setItem('__user_name__', username);
            localStorage.setItem('_user_role_', response.role);
            localStorage.setItem('_user_id_', response.user_id);
            if (remember) {
              let sessionCookie = document.cookie.split('; ').find(row => row.startsWith('session='));
              if (sessionCookie) {
                let expireDate = new Date();
                expireDate.setDate(expireDate.getDate() + 7); // Set cookie to expire in 7 days
                document.cookie = `${sessionCookie}; expires=${expireDate.toUTCString()}; path=/`;
              }
            }
            return response;
          }).catch(error => { throw error; });
      }).catch(error => { throw error; });
  },
  async register(context, { username, password }) { return await api.register(username, password) },
  async getNews(context, { page }) { return await api.getnews(page); },
  async getPosts(context, {pay, sort_by, key_word, tags, page}) { return await api.getPosts(pay, sort_by, key_word, tags, page); },
  async getTags(context, {key_word}) { return await api.getTags(key_word); },
  async createPost(context, {title, content, tags, cost, link}) { return await api.createPost(title, content, tags, cost, link); },
  async getPost(context, {id}) { return await api.getPostDetail(id); },
  async getUserProfile(context, {id}) { return await api.getUserProfile(id); },
  async getTasks(context, {tags, sort_by, key_word, page}) { return await api.getTasks(tags, sort_by, key_word, page); },
  async createTask(context, {title, content, tags, commission}) { return await api.createTask(title, content, tags, commission); },
  async likePost(context, {id}) { return await api.likePost(id); },
  async dislikePost(context, {id}) { return await api.dislikePost(id); },
  async notLikePost(context, {id}) { return await api.notLikePost(id); },
  async notDislikePost(context, {id}) { return await api.notDislikePost(id); },
  async favourPost(context, {id}) { return await api.favourPost(id); },
  async notFavourPost(context, {id}) { return await api.notFavourPost(id); },
  async getPostComments(context, {id}) { return await api.getPostComments(id); },
  async followUser(context, {id}) { return await api.followUser(id); },
  async notFollowUser(context, {id}) { return await api.notFollowUser(id); },
  async createComment(context, {id, content, parent_id}) { return await api.createComment(id, content, parent_id); },
  async getFollows(context, {id}) { return await api.getFollows(id); },
  async ownPosts(context) { return await api.ownPosts(); },
  async modifyUser(context, {id, password, email, signature}) { return await api.modifyUser(id, password, email, signature); },
  async publishAnnouncement(context, {title, content}) { return await api.publishAnnouncement(title, content); },
  async getAllUsers(context) { return await api.getAllUsers(); },
  async blockUser(context, {id}) { return await api.blockUser(id); },
  async unblockUser(context, {id}) { return await api.unblockUser(id); },
  async getFavorites(context, {id}) { return await api.getFavorites(id); },
  async getTaskDetail(context, {id}) { return await api.getTaskDetail(id); },
  async getTaskSubmits(context, {id}) { return await api.getTaskSubmits(id); },
  async submitTask(context, {id, profile, bhpan_url}) { return await api.submitTask(id, profile, bhpan_url); },
  async payForPost(context, {id}) { return await api.payForPost(id); },
  async deletePost(context, {id}) { return await api.deletePost(id); },
  async modifyPost(context, {id, title, content, tags, cost, bhpan_url}) { return await api.modifyPost(id, title, content, tags, cost, bhpan_url); },
  async ownTasks(context) { return await api.ownTasks(); },
  async deleteTask(context, {id}) { return await api.deleteTask(id); },
  async modifyTask(context, {id, title, content, tags, commission}) { return await api.modifyTask(id, title, content, tags, commission); },
  async confirmTask(context, {task_id, submit_id}) { return await api.confirmTask(task_id, submit_id); },
  async uploadFile(context, {file}) { return await api.uploadFile(file); },
  async getChart(context) { return await api.getChart(); },
  async getNew(context) { return await api.getNew(); }
};
