<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-center" v-if="media">{{ media.title }}</h1>
        <p v-if="media">{{ media.description }}</p>
        <v-progress-circular v-else indeterminate color="primary" class="mx-auto"></v-progress-circular>

        <div v-if="media && media.content" class="media-box">
          <div v-if="isImage(media.content)">
            <v-img :src="media.content" :alt="media.title" class="media-view"></v-img>
          </div>
          <v-responsive v-else class="media-view">
            <video controls :src="media.content" class="video-view"></video>
          </v-responsive>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <h2 class="text-center">Chat</h2>

        <v-progress-circular v-if="loadingChats" indeterminate color="primary" class="mx-auto"></v-progress-circular>

        <p v-if="!chats.length && !loadingChats" class="text-center">No comments yet</p>
        <p v-if="media && media.chats_count" class="text-center">{{ media.chats_count }} Chats </p>

        <div v-if="chats.length" class="chats-container">
          <v-card v-for="chat in chats" :key="chat.id" :class="getUserColor(chat.owner)" class="chat-box mb-3">
            <v-card-title>
              {{ chat.owner }}
            </v-card-title>
            <v-card-text>
              {{ chat.content }}
            </v-card-text>
          </v-card>
        </div>

        <v-btn v-if="nextPageUrl" @click="loadMoreChats" color="primary">Load More Chats</v-btn>

        <v-form v-if="media" @submit.prevent="submitChat">
          <v-textarea v-model="newChat" label="Add a chat" outlined rows="3" required></v-textarea>
          <v-btn type="submit" color="primary" :disabled="isSubmitting">Post Chat</v-btn>
        </v-form>
      </v-col>
    </v-row>

    <v-snackbar v-model="snackbar.visible" :timeout="snackbar.timeout" :color="snackbar.color">
      {{ snackbar.message }}
      <v-btn color="white" text @click="snackbar.visible = false">Close</v-btn>
    </v-snackbar>
  </v-container>
</template>

<script>
export default {
  name: 'MediaDetail',
  data() {
    return {
      media: null,
      chats: [],
      newChat: '',
      isSubmitting: false,
      loadingChats: true,
      nextPageUrl: null,
      snackbar: {
        visible: false,
        message: '',
        color: 'success',
        timeout: 3000,
      },
    };
  },
  async created() {
    const mediaId = this.$route.params.medias_id;
    try {
      const response = await this.$axios.get(`/medias/${mediaId}/`);
      console.log('Media Response:', response.data);
      this.media = response.data;

      await this.loadChats();
    } catch (error) {
      console.error('Error fetching media or chats:', error);
      this.snackbar.message = 'Failed to fetch media or chats, please try again.';
      this.snackbar.color = 'error';
      this.snackbar.visible = true;
    } finally {
      this.loadingChats = false;
    }
  },
  methods: {
    isImage(filePath) {
      return /\.(jpeg|jpg|gif|png)$/.test(filePath);
    },
    getUserColor(owner) {
      const hash = Array.from(owner).reduce((acc, char) => acc + char.charCodeAt(0), 0);
      const colorIndex = hash % 4;
      const colors = ['green lighten-3', 'blue lighten-3', 'purple lighten-3', 'orange lighten-3'];
      return colors[colorIndex] || 'grey lighten-3';
    },
    async loadChats() {
      this.loadingChats = true;
      const mediaId = this.$route.params.medias_id;
      try {
        const response = await this.$axios.get(`/medias/${mediaId}/chats/`);
        console.log('Chats Response:', response.data.results);
        this.chats = response.data.results || [];
        this.nextPageUrl = response.data.next;
      } catch (error) {
        console.error('Error fetching chats:', error);
        this.snackbar.message = 'Failed to load chats.';
        this.snackbar.color = 'error';
        this.snackbar.visible = true;
      } finally {
        this.loadingChats = false;
      }
    },
    async loadMoreChats() {
      if (this.nextPageUrl) {
        this.loadingChats = true;
        try {
          const response = await this.$axios.get(this.nextPageUrl);
          this.chats.push(...response.data.results);
          this.nextPageUrl = response.data.next;
        } catch (error) {
          console.error('Error loading more chats:', error);
          this.snackbar.message = 'Failed to load more chats.';
          this.snackbar.color = 'error';
          this.snackbar.visible = true;
        } finally {
          this.loadingChats = false;
        }
      }
    },
    async submitChat() {
      if (this.newChat.trim()) {
        this.isSubmitting = true;
        const mediaId = this.$route.params.medias_id;
        try {
          const response = await this.$axios.post(`/medias/${mediaId}/chats/`, {
            content: this.newChat,
          });
          this.chats.unshift(response.data);
          this.newChat = '';
        } catch (error) {
          console.error('Error posting chat:', error);
          this.snackbar.message = 'Failed to post your chat, please try again.';
          this.snackbar.color = 'error';
          this.snackbar.visible = true;
        } finally {
          this.isSubmitting = false;
        }
      } else {
        alert('Please enter a chat before submitting.');
      }
    },
  },
};
</script>

<style scoped>
.media-box {
  border: 2px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  max-width: 800px;
  margin: 0 auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: white;
}

.media-view {
  width: 100%;
  height: auto;
  object-fit: contain;
}

.video-view {
  max-width: 100%;
  height: auto; 
}

.chat-box {
  padding: 10px;
  border-radius: 8px;
}

.chats-container {
  margin-top: 20px;
}

.chat-form {
  margin-top: 20px;
}
</style>