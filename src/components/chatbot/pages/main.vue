<template>
    <div class="main">

        <div class="chats-scroll">
            <ul class="chat-list">
                <li v-for="chat in chats">
                    <p>{{chat.name}}</p>
                </li>
            </ul>
        </div>

        <div class="messsages-area">

        </div>

        <div class="chat-box">
            <input type="text"/>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const chats = ref([])
</script>
