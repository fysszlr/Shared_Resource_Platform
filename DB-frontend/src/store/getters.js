// $store.getters.hasParticles
export default {
    hasParticles(state) {
      return state.hasParticles;
    },
    username: state => state._user_name_ == null ? "UnauthorizedUser" : state._user_name_,
    user_id: state => state._user_id_,
};