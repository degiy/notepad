<template>
  <v-textarea  v-model="content" class="editor-textarea" @input="updatePreview" :rows="numberOfRows">
  </v-textarea>

</template>
  
<script setup>
import { ref, watch, onMounted, defineProps, defineExpose } from 'vue';

// Define props
const props = defineProps({
  content: String
});

const content = ref(props.content);

// Watch for changes in props.content
watch(() => props.content, (newContent) => {
  content.value = newContent;
});


// Function to update the HTML preview
const updatePreview = () => {
  console.log("update")
  };

// Watch for changes in markdown and update preview
watch(content, updatePreview, { immediate: true });

const numberOfRows = ref(2); // Default number of rows

const calculateTextareaRows= (height) => {
    const lineHeight = 20; // Adjust this value to match the line-height of the textarea
    numberOfRows.value = Math.floor(height / lineHeight);
    console.log(`Calculated number of rows: ${numberOfRows.value} from ${height}`);
}

defineExpose({
  calculateTextareaRows
});

onMounted(() => {

});


</script>
  
  <style>
  .editor-textarea {
    background-color: #ffc;
    line-height: 20px;
}

  </style>
  