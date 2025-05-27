import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useErrorStore } from "@/stores/error";
import { useRouter } from "vue-router";
import avatarNoneAssetURL from "@/assets/avatar-none.png";

export const useAuthStore = defineStore("auth", () => {
  const router = useRouter();
  const storeError = useErrorStore();
  const user = ref(null);
  const token = ref("");

  const userName = computed(() => {
    return user.value ? user.value.name : "";
  });

  const userFirstLastName = computed(() => {
    const names = userName.value.trim().split(" ");
    const firstName = names[0] ?? "";
    const lastName = names.length > 1 ? names[names.length - 1] : "";
    return (firstName + " " + lastName).trim();
  });

  const userEmail = computed(() => {
    return user.value ? user.value.email : "";
  });

  const userPhotoUrl = computed(() => {
    const photoFile = user.value ? user.value.photoFileName ?? "" : "";
    if (photoFile) {
      return axios.defaults.baseURL.replaceAll("/api", photoFile);
    }
    return avatarNoneAssetURL;
  });

  // This function is "private" - not exported by the store
  const clearUser = () => {
    resetIntervalToRefreshToken()
    user.value = null
    token.value = ''
    localStorage.removeItem('token')
    axios.defaults.headers.common.Authorization = ''
  };

  const login = async (credentials) => {
    storeError.resetMessages();
    try {
      const responseLogin = await axios.post("auth/login", credentials);
      token.value = responseLogin.data.token;
      localStorage.setItem('token', token.value);
      axios.defaults.headers.common.Authorization = "Bearer " + token.value;
      const responseUser = await axios.get("users/me");
      user.value = responseUser.data.data;
      repeatRefreshToken();
      router.push({ name: "main" });
      return user.value;
    } catch (e) {
      clearUser();
      storeError.setErrorMessages(
        e.response.data.message,
        e.response.data.errors,
        e.response.status,
        "Authentication Error!"
      );
      return false;
    }
  };
  const logout = async () => {
    storeError.resetMessages();
    try {
      await axios.post("auth/logout");
      clearUser();
      return true;
    } catch (e) {
      clearUser();
      storeError.setErrorMessages(
        e.response.data.message,
        [],
        e.response.status,
        "Authentication Error!"
      );
      return false;
    }
  };
  // These 2 functions and intervalToRefreshToken variable are "private" - not exported
  let intervalToRefreshToken = null;
  const resetIntervalToRefreshToken = () => {
    if (intervalToRefreshToken) {
      clearInterval(intervalToRefreshToken);
    }
    intervalToRefreshToken = null;
  };
  const repeatRefreshToken = () => {
    if (intervalToRefreshToken) {
      clearInterval(intervalToRefreshToken);
    }
    intervalToRefreshToken = setInterval(async () => {
      try {
        const response = await axios.post("auth/refreshtoken");
        token.value = response.data.token;
        localStorage.setItem('token', token.value)
        axios.defaults.headers.common.Authorization = "Bearer " + token.value;
        return true;
      } catch (e) {
        clearUser();
        storeError.setErrorMessages(
          e.response.data.message,
          e.response.data.errors,
          e.response.status,
          "Authentication Error!"
        );
        return false;
      }
    }, 1000 * 60 * 110); // repeat every 110 minutes
    // To test the refresh token, replace previous line with the following code
    // This will repeat the refreshtoken endpoint every 10 seconds:
    //}, 1000 * 10)
    return intervalToRefreshToken;
  };
  const restoreToken = async function () {
    let storedToken = localStorage.getItem('token');
    if (storedToken) {
      try {
        token.value = storedToken;
        axios.defaults.headers.common.Authorization = 'Bearer ' + token.value;
        const responseUser = await axios.get('users/me');
        user.value = responseUser.data.data;
        repeatRefreshToken();
        return true;
      } catch {
        clearUser();
        return false;
      }
    }
    return false;
  };

  const getTables = async function () {
    try {
      const response = await axios.get('users/me/table', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar tabelas:', error.response?.data?.message || error.message);
      throw error;
    }
  };

  const addTable = async function (table) {
    try {
      const response = await axios.post('users/me/add-table', { table });

      console.log('Tabela adicionada com sucesso:', response.data.message);

      return response.data.message;
    } catch (error) {

      console.error('Erro ao adicionar tabela:', error.response?.data?.message || error.message);

      throw error;
    }
  };
  
  return {
    user,
    userName,
    userEmail,
    userPhotoUrl,
    restoreToken,
    login,
    logout,
    getTables,
    addTable,
  };
});
