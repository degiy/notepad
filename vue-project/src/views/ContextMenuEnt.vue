<template>
  <div class="context-menu-ent" :style="{ top: position.y + 'px', left: position.x + 'px' }">
    <v-list>
      <v-list-item @click="refresh">
        <v-list-item-title>Reload from server</v-list-item-title>
      </v-list-item>


      <v-list-item title="---"/>

      <v-list-item @click="deleteEnt" v-if="selectedEnt && (! entDialVisible) && (! entDialVisible)">
        <v-list-item-title>Delete</v-list-item-title>
      </v-list-item>
    </v-list>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  position: Object,
  selectedEnt: Object,
});

const emit = defineEmits(['delete', 'refresh', 'move']);
const entDialVisible = ref(false);

onMounted(() => {
  entDialVisible.value = false;
});

const refresh = () => {
  emit('refresh');
}; 

const deleteEnt = () => {
  emit('delete');
};


const closeAddEntDialog = () => {
  entDialVisible.value = false;
  entEntName.value = '';
};

</script>

<style scoped>
.context-menu-ent {
  position: absolute;
  z-index: 1000;
  background: white;
  border: 1px solid #ccc;
  padding: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
</style>
