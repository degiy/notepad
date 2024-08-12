<template>
  <div class="context-menu-dir" :style="{ top: position.y + 'px', left: position.x + 'px' }">
    <v-list>
      <v-list-item @click="refresh">
        <v-list-item-title>Reload from server</v-list-item-title>
      </v-list-item>

      <v-list-item title="---"/>

      <v-list-item @click="addDir">
        <v-list-item-title>Add New Directory</v-list-item-title>
      </v-list-item>
      <v-list-item v-if="dirDialVisible">
       <v-text-field ref="newDirInput" v-model="newDirName" label="Directory Name" @keyup.enter="handleAddDir"
          @click.stop></v-text-field>
        <v-btn @click="handleAddDir">Add</v-btn>
        <v-btn @click="closeAddDirDialog">Cancel</v-btn>
      </v-list-item>

      <v-list-item @click="addEnt">
        <v-list-item-title>Create new item</v-list-item-title>
      </v-list-item>
      <v-list-item v-if="entDialVisible">
       <v-text-field ref="newEntInput" v-model="newEntName" label="New note name" @keyup.enter="handleAddEnt"
          @click.stop></v-text-field>
        <v-btn @click="handleAddEnt">Create</v-btn>
        <v-btn @click="closeAddEntDialog">Cancel</v-btn>
      </v-list-item>

      <v-list-item title="---"/>

      <v-list-item @click="deleteDir" v-if="selectedDir && (! dirDialVisible) && (! entDialVisible)">
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
  selectedDir: Object,
});

const emit = defineEmits(['delete', 'add', 'refresh', 'adde']);
const dirDialVisible = ref(false);
const newDirName = ref('');
const newDirInput = ref(null);

onMounted(() => {
  dirDialVisible.value = false;
});

const refresh = () => {
  emit('refresh');
} 

const deleteDir = () => {
  emit('delete');
};

const addDir = () => {
  event.stopPropagation(); // Prevents the menu from closing
  dirDialVisible.value = true;
  nextTick(() => {
    // Focus the text field after the DOM has updated
    if (newDirInput.value) {
      newDirInput.value.focus();
    }
  });
};

const closeAddDirDialog = () => {
  dirDialVisible.value = false;
  newDirName.value = '';
};

const handleAddDir = () => {
  if (newDirName.value.trim() !== '') {
    console.log("dir name to create is ",newDirName.value);
    emit('add', newDirName.value);
    closeAddDirDialog();
  }
};

// ========= create new entry (aka note) ========

const entDialVisible = ref(false);
const newEntName = ref('');
const newEntInput = ref(null);

const addEnt = () => {
  event.stopPropagation(); // Prevents the menu from closing
  entDialVisible.value = true;
  nextTick(() => {
    // Focus the text field after the DOM has updated
    if (newEntInput.value) {
      newEntInput.value.focus();
    }
  });
};

const handleAddEnt = () => {
  if (newEntName.value.trim() !== '') {
    console.log("note name to create is ",newEntName.value);
    emit('adde', newEntName.value);
    closeAddDirDialog();
  }
};

const closeAddEntDialog = () => {
  entDialVisible.value = false;
  entDirName.value = '';
};

</script>

<style scoped>
.context-menu-dir {
  position: absolute;
  z-index: 1000;
  background: white;
  border: 1px solid #ccc;
  padding: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
</style>
