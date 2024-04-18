// chatbot.js
import { v4 as uuidv4 } from 'http://172.20.67.24:8081/uuidv4';
export default {
    template: `
    <div>
      <!-- First Component -->
      <section class="bottom-section">
        <img src="images/eu.png" height="35" style="margin-right: 1rem">
            <div class="chat" @click="changeVisibility()">
                <transition name="fade" mode="out-in">
                    <svg
                    style="fill: #036; margin-top: 3px"
                    v-if="!showChatbot"
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    >
                    <!-- Chat SVG -->
                    <path d="M3 3h18v12H7l-4 4z" />
                    </svg>
                    <svg
                    style="fill: #036"
                    v-else
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    >
                    <!-- Exit SVG -->
                    <path
                        d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
                    />
                    </svg>
                </transition>
            </div>
        </section>
        <Transition name="fade">
            <div v-if="showChatbot" class="chatbot-container" style="position:relative">
                <!-- Second Component -->
                <div v-if="showChatbot" class="container" :class="{ minimized: minimized }">
                    <div>
                        <div class="top" style="padding: 0 0 0 13px;border:unset;background-color:unset">
                            <div class="AvatarBot">
                                <svg style="height:30px;width:30px" version="1.1" id="svg1" width="468" height="429.33334" viewBox="0 0 468 429.33334" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg"> <defs id="defs1" /> <g id="g1"> <image width="468" height="429.33334" preserveAspectRatio="none" xlink:href="data:image/png;base64,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&#10;" id="image1" /> </g></svg>
                            </div>
                            <div class="InfoBot">
                                <p class="TitleBot" style="margin-top:unset">Virtualni asistent</p>
                                <p class="status" style="margin-top:unset">e-Predmet</p>
                            </div>
                            <div style="display: flex;right: 0;position: absolute;padding-right: 16px;">
                                <button type="button" class="controls" @click="refresh">
                                    <svg focusable="false" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 32 32" aria-hidden="true"><path d="M26,18A10,10,0,1,1,16,8h6.1821l-3.5844,3.5854L20,13l6-6L20,1,18.5977,2.414,22.1851,6H16A12,12,0,1,0,28,18Z"></path></svg>
                                </button>
                                <button type="button" class="controls" @click="toggleMinimized">
                                    <template v-if="minimized">
                                        <svg focusable="false" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" fill="currentColor" aria-hidden="true" width="24" height="24" viewBox="0 0 32 32" class="bx--btn__icon"><path d="M17 15L17 8 15 8 15 15 8 15 8 17 15 17 15 24 17 24 17 17 24 17 24 15z"></path></svg>
                                    </template>
                                    <template v-else>
                                        <svg focusable="false" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="24" height="24" viewBox="0 0 32 32" aria-hidden="true"><path d="M8 15H24V17H8z"></path></svg>
                                    </template>
                                </button>
                            </div>
                        </div>
                        <div class="ContentChat" ref="chatContainer">
                            <transition-group name="message" tag="div">
                                <div
                                    v-for="(message, index) in messages"
                                    :key="index"
                                    :class="message.classes"
                                    :data-user="message.dataUser"
                                    v-html="message.text"
                                />
                            </transition-group>
                            <section v-if="status_func_SendMsgBot === 1">
                                <div class="captionBot msgCaption" data-user="false"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <rect x="3" y="11" width="18" height="10" rx="2"></rect> <circle cx="12" cy="5" r="2"></circle> <path d="M12 7v4"></path> <line x1="8" y1="16" x2="8" y2="16"></line> <line x1="16" y1="16" x2="16" y2="16"></line> </g></svg> <span style="margin-top:2px">Virtualni asistent</span></div>
                                <div class="message"> <div class="bot-response text" text-first="true"><svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="24px" height="30px" viewBox="0 0 24 30" style="enable-background:new 0 0 50 50;" xml:space="preserve"> <rect x="0" y="0" width="4" height="10" fill="rgb(155, 166, 178)"> <animateTransform attributeType="xml" attributeName="transform" type="translate" values="0 0; 0 20; 0 0" begin="0" dur="0.6s" repeatCount="indefinite"> </animateTransform> </rect> <rect x="10" y="0" width="4" height="10" fill="rgb(155, 166, 178)"> <animateTransform attributeType="xml" attributeName="transform" type="translate" values="0 0; 0 20; 0 0" begin="0.2s" dur="0.6s" repeatCount="indefinite"> </animateTransform> </rect> <rect x="20" y="0" width="4" height="10" fill="rgb(155, 166, 178)"> <animateTransform attributeType="xml" attributeName="transform" type="translate" values="0 0; 0 20; 0 0" begin="0.4s" dur="0.6s" repeatCount="indefinite"> </animateTransform> </rect> </svg></div> </div>
                            </section>
                            <!-- SVG icons for thumbs up and thumbs down -->
                            <div v-if="showFeedbackButtons" style="padding: 0 25px 0px;">
                                <button class="thumb" :disabled="selectedFeedbackButton" :style="selectedFeedbackButton === 'up' ? { transform: 'scale(1)', opacity: '1' } : {}" @click="handleFeedback(true)">
                                    <svg style="padding:15px 5px;height:25px;width:25px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M3 10C3 9.44772 3.44772 9 4 9H7V21H4C3.44772 21 3 20.5523 3 20V10Z" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> <path d="M7 11V19L8.9923 20.3282C9.64937 20.7662 10.4214 21 11.2111 21H16.4586C17.9251 21 19.1767 19.9398 19.4178 18.4932L20.6119 11.3288C20.815 10.1097 19.875 9 18.6391 9H14" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> <path d="M14 9L14.6872 5.56415C14.8659 4.67057 14.3512 3.78375 13.4867 3.49558V3.49558C12.6336 3.21122 11.7013 3.59741 11.2992 4.4017L8 11H7" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>
                                </button>
                                <button class="thumb" :disabled="selectedFeedbackButton" :style="selectedFeedbackButton === 'down' ? { transform: 'scale(1)', opacity: '1' } : {}" @click="handleFeedback(false)">
                                    <svg style="padding:15px 5px;height:25px;width:25px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M21 14C21 14.5523 20.5523 15 20 15H17V3H20C20.5523 3 21 3.44772 21 4V14Z" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> <path d="M17 13V5L15.0077 3.6718C14.3506 3.23375 13.5786 3 12.7889 3H7.54138C6.07486 3 4.82329 4.06024 4.5822 5.5068L3.38813 12.6712C3.18496 13.8903 4.12504 15 5.36092 15H10" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> <path d="M10 15L9.31283 18.4358C9.13411 19.3294 9.64876 20.2163 10.5133 20.5044V20.5044C11.3664 20.7888 12.2987 20.4026 12.7008 19.5983L16 13H17" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>
                                </button>
                            </div>
                        </div>
                        <div class="BoxSentMSG " ref="messageBox">
                            <textarea
                                ref="textarea"
                                v-if="!showOptions"
                                placeholder="Napišite poruku..."
                                class="InputMSG"
                                @input="adjustTextareaHeight"
                                v-model="inputValue"
                                @keydown.enter="sendMessage"
                                required
                                maxlength="200"
                            />
                            <div v-else>
                                <!-- Render chatbot options here when showOptions is true -->
                                <div v-html="chatbotOptions"></div>
                            </div>
                            <div class="send-icon" @click="sendMessage"><svg id="send1" :class="{ 'none': status_func_SendMsgBot }" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24 " xml:space="preserve"> <path fill="#d7d7d7 " d="M22,11.7V12h-0.1c-0.1,1-17.7,9.5-18.8,9.1c-1.1-0.4,2.4-6.7,3-7.5C6.8,12.9,17.1,12,17.1,12H17c0,0,0-0.2,0-0.2c0,0,0,0,0,0c0-0.4-10.2-1-10.8-1.7c-0.6-0.7-4-7.1-3-7.5C4.3,2.1,22,10.5,22,11.7z "> </path> </svg> <svg id="send2" :class="{ 'none': !status_func_SendMsgBot }" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="24px" height="30px" viewBox="0 0 24 30" style="enable-background:new 0 0 50 50;" xml:space="preserve"> <rect x="0" y="10" width="4" height="10" fill="#333" opacity="0.2"> <animate attributeName="opacity" attributeType="XML" values="0.2; 1; .2" begin="0s" dur="0.6s" repeatCount="indefinite"></animate> <animate attributeName="height" attributeType="XML" values="10; 20; 10" begin="0s" dur="0.6s" repeatCount="indefinite"></animate> <animate attributeName="y" attributeType="XML" values="10; 5; 10" begin="0s" dur="0.6s" repeatCount="indefinite"></animate> </rect> <rect x="8" y="10" width="4" height="10" fill="#333" opacity="0.2"> <animate attributeName="opacity" attributeType="XML" values="0.2; 1; .2" begin="0.15s" dur="0.6s" repeatCount="indefinite"></animate> <animate attributeName="height" attributeType="XML" values="10; 20; 10" begin="0.15s" dur="0.6s" repeatCount="indefinite"></animate> <animate attributeName="y" attributeType="XML" values="10; 5; 10" begin="0.15s" dur="0.6s" repeatCount="indefinite"></animate> </rect> <rect x="16" y="10" width="4" height="10" fill="#333" opacity="0.2"> <animate attributeName="opacity" attributeType="XML" values="0.2; 1; .2" begin="0.3s" dur="0.6s" repeatCount="indefinite"></animate> <animate attributeName="height" attributeType="XML" values="10; 20; 10" begin="0.3s" dur="0.6s" repeatCount="indefinite"></animate> <animate attributeName="y" attributeType="XML" values="10; 5; 10" begin="0.3s" dur="0.6s" repeatCount="indefinite"></animate> </rect> </svg> </div>
                        </div>
                        <Transition name="fade">
                            <div v-if="showStars" class="feedback-modal">
                                <!-- Feedback modal content -->
                                <div class="modal-content">
                                    <button @click="closeFeedBack" class="exit-button"><svg focusable="false" preserveAspectRatio="xMidYMid meet"xmlns="http://www.w3.org/2000/svg" fill="black" aria-hidden="true" width="20" height="20" viewBox="0 0 32 32"><path d="M24 9.4L22.6 8 16 14.6 9.4 8 8 9.4 14.6 16 8 22.6 9.4 24 16 17.4 22.6 24 24 22.6 17.4 16 24 9.4z"/></svg></button>
                                    <div class="survey">
                                        <div style="text-align:center">
                                            <span>Kako biste ocijenili Vaše iskustvo s Virtualnim asistentom?</span>
                                            <div class="rating-question">
                                                <div class="star-rating">
                                                    <input v-model="selectedStars" type="radio" id="5-stars" name="rating" value="5" />
                                                    <label for="5-stars" class="star">&#9733;</label>
                                                    <input v-model="selectedStars" type="radio" id="4-stars" name="rating" value="4" />
                                                    <label for="4-stars" class="star">&#9733;</label>
                                                    <input v-model="selectedStars" type="radio" id="3-stars" name="rating" value="3" />
                                                    <label for="3-stars" class="star">&#9733;</label>
                                                    <input v-model="selectedStars" type="radio" id="2-stars" name="rating" value="2" />
                                                    <label for="2-stars" class="star">&#9733;</label>
                                                    <input v-model="selectedStars" type="radio" id="1-star" name="rating" value="1" />
                                                    <label for="1-star" class="star">&#9733;</label>
                                                </div>
                                            </div>
                                        </div>
                                        <div>
                                            <span>Molimo podijelite Vaše mišljenje o iskustvu čavrljanja.</span>
                                            <div>
                                                <label></label>
                                                <div>
                                                    <textarea id="survey-textarea" v-model="comment" aria-required="false"></textarea>
                                                    <span></span>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="submit-survey">
                                            <button @click="sendStarsFeedback" type="button" :disabled="this.selectedStars == 0">
                                                <pre>Pošalji anketu</pre>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </Transition>
                    </div>
                </div>
            </div>
        </Transition>
    </div>
  `,
    data() {
        return {
            inputValue: '',
            messages: [],
            status_func_SendMsgBot: 0,
            showOptions: false, // Add this property to control input/option visibility
            chatbotOptions: '',
            showFeedbackButtons: false,
            selectedFeedbackButton: false,
            responseApi: {},
            minimized: false,
            intent_id: '',
            conditions: {},
            sessionUUID: '',
            showChatbot: false,
            system_initial: '',
            showStars: false,
            selectedStars: 0,
            comment: "",
        };
    },
    watch: {
        showChatbot(newValue) {
            if (newValue) {
                this.$nextTick(() => {
                    const responseContainer = this.$refs.messageBox;

                    responseContainer.addEventListener('click', (event) => {
                        if (event.target.classList.contains('bot-option')) {
                            const optionText = event.target.innerText;
                            const text = event.target.getAttribute('data-text');
                            this.handleUserResponse(optionText, text);
                        }
                    });

                    const chatContainer = this.$refs.chatContainer;

                    chatContainer.addEventListener('click', async (event) => {
                        let response = '';
                    
                        if (event.target.classList.contains('bot-option')) {
                            if (!(event.target.getAttribute('data-text') == 'PRETRAŽI BAZU ZNANJA' || event.target.getAttribute('data-text') == 'PREFORMULIRAT ĆU PITANJE')) {
                                this.addUserMessage(event.target.getAttribute('data-text'));
                                response = await fetch('http://172.20.67.24:8081/getRulesForIntent?intent_id=' + event.target.getAttribute('data-intent-id') + '&system_id=1', {
                                        method: 'GET',
                                    })
                                    .then(response => {
                                        if (!response.ok) {
                                            throw new Error(response.error);
                                        }
                                        return response.json();
                                    })
                                    .then(data => JSON.parse(data)[0]);
                    
                                response.intent_id = event.target.getAttribute('data-intent-id');
                                response.position = 0;
                                this.intent_id = event.target.getAttribute('data-intent-id');
                                this.selectedFeedbackButton = false;
                                this.addBotMessage(response);
                            } else if (event.target.getAttribute('data-text') == 'PREFORMULIRAT ĆU PITANJE') {
                                response = {
                                    assistant_answer: `Možda mogu ponuditi bolji odgovor ako preformulirate Vaše pitanje.`,
                                };
                                this.addBotMessage(response);
                            } else {
                                this.addUserMessage(event.target.getAttribute('data-text'));
                                let response_tmp = await fetch('http://172.20.67.24:8081/searchDocuments', {
                                        method: "POST",
                                        headers: {
                                            'Accept': 'application/json',
                                            'Content-Type': 'application/json',
                                        },
                                        body: JSON.stringify({
                                            text: event.target.getAttribute('data-question'),
                                            systemID: "1",
                                        }),
                                    })
                                    .then((response) => {
                                        if (!response.ok) {
                                            throw new Error(response.error);
                                        }
                                        return response.json();
                                    });
                    
                                if (Number(response_tmp.threshold) > Number(response_tmp.score) * 100) {
                                    response = {
                                        assistant_answer: `<section><p>Nismo pronašli niti jedan dokument koji odgovara Vašem pitanju. Molim Vas pokušajte ponovno.</p><section style="font-style:italic">${response_tmp.text}</section></section>`,
                                    };
                                } else {
                                    response = {
                                        assistant_answer: `<section><p>U našoj bazi pronašli smo sljedeći dokument s najvećim podudaranjem:</p><h4>${response_tmp.document_title}${response_tmp.document_page ? `(${response_tmp.document_page}.str)` : ''}</h4><section>...</section><section style="font-style:italic">${response_tmp.text}</section><section>...</section></section>`,
                                    };
                                    this.addBotMessage({ assistant_answer: response });
                                }
                            }
                    
                            console.log(response);
                    
                            await fetch('http://172.20.67.24:8081/updateConversationTmp', {
                                    method: "POST",
                                    headers: {
                                        'Accept': 'application/json',
                                        'Content-Type': 'application/json',
                                    },
                                    body: JSON.stringify({ uuid: this.sessionUUID, system_id: "1", intent_id: Number(event.target.getAttribute('data-intent-id')), question: event.target.getAttribute('data-question'), threshold: event.target.getAttribute('data-threshold'), response: response }),
                                })
                                .then((response) => {
                                    if (!response.ok) {
                                        throw new Error(response.error);
                                    }
                                    return response.json();
                                });
                    
                            // Disable all options after the user makes a selection and change the style of the selected button
                            const allOptions = document.querySelectorAll(`.bot-option[data-intent-id="${event.target.getAttribute('data-intent-id')}"]`);
                            allOptions.forEach((optionElement) => {
                                if (optionElement.innerText.toUpperCase() === event.target.getAttribute('data-text').toUpperCase()) {
                                    optionElement.classList.add('selected');
                                }
                            });
                        }
                    });
                });
            }
        },
    },

    methods: {
        async initializeBot() {
            // Simulate a delayed bot response after initial greeting
            await new Promise(resolve => setTimeout(resolve, 1000));
            const responseMessage = {
                assistant_answer: this.system_initial
            };
            this.addBotMessage(responseMessage);
            // ADD SUBJECTS IN THE BEGGINING
            let themes = await fetch('http://172.20.67.24:8081/getThemes?system_id=1', {
                method: 'GET',
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(response.error);
                }
                return response.json();
            })
            if(themes[0].intents){
                const optionsHtml = JSON.parse(themes[0].intents).map(option => `<button class="bot-option" data-intent-id="${option.key}" data-text="${option.name}" data-question="${option.name}" data-threshold="1.0">${option.name}</button>`).join('');
                this.messages.push({
                    text: optionsHtml,
                    classes: ['message'],
                    dataUser: false,
                });
            }
        },

        async sendMessage() {
            this.showFeedbackButtons = false
            if (this.inputValue !== '' && this.status_func_SendMsgBot === 0) {
                // Sanitize the input to allow only plain text
                const sanitizedInput = DOMPurify.sanitize(this.inputValue, { ALLOWED_TAGS: [] });
                // Add the sanitized input as a user message
                this.addUserMessage(sanitizedInput);

                try {
                    // Check the response type
                    if (this.responseApi.response_type === 'Slobodni tekst') {
                        if (this.responseApi.continuation === 'Vrati se na pod-akciju') {
                            let response = await fetch('http://172.20.67.24:8081/goToStep?intent_id=' + this.responseApi.intent_id + '&system_id=1' + '&id=' + this.responseApi.previous_response.id, {
                                    method: 'GET',
                                })
                                .then(response => {
                                    if (!response.ok) {
                                        throw new Error(response.error);
                                    }
                                    return response.json();
                                })
                                .then(data => JSON.parse(data)[0]);
                            response.intent_id = this.responseApi.intent_id
                            this.selectedFeedbackButton = false;
                            this.addBotMessage(response)
                        } else if (this.responseApi.continuation === 'Nastavite na idući korak') {
                            let condition = {
                                subject: this.responseApi.assistant_answer,
                                predicate: 'je',
                                object: "defined",
                            }
                            // Push the condition into the session's conditions array
                            this.conditions[this.sessionUUID].push(condition);
                            const response = await fetch('http://172.20.67.24:8081/userResponse', {
                                    method: "POST",
                                    headers: {
                                        'Accept': 'application/json',
                                        'Content-Type': 'application/json'
                                    },
                                    body: JSON.stringify({
                                        conditions: this.conditions[this.sessionUUID],
                                        intent_id: this.responseApi.intent_id,
                                        id: this.responseApi.position,
                                        uuid: this.sessionUUID,
                                        systemID: "1",
                                        answer: sanitizedInput
                                    })
                                })
                                .then((response) => {
                                    if (!response.ok) {
                                        throw new Error(response.error)
                                    }
                                    return response.json();
                                })
                            response.intent_id = this.responseApi
                            this.addBotMessage(response);
                        } else if (this.responseApi.continuation === 'Završetak radnje') {
                            this.responseApi = {}
                            this.showFeedbackButtons = true
                        }
                        else if(this.responseApi.continuation === 'Kontaktirajte agenta'){
                            try {
                              let condition = {
                                subject: this.responseApi.assistant_answer,
                                predicate: 'je',
                                object: "defined",
                              }
                              // Push the condition into the session's conditions array
                              this.conditions[this.sessionUUID].push(condition);
                              

                              const response = await fetch('http://172.20.67.24:8081/sendMail', {
                                    method: "POST",
                                    headers: {
                                        'Accept': 'application/json',
                                        'Content-Type': 'application/json'
                                    },
                                    body: JSON.stringify({
                                        response: this.responseApi,
                                        session_id: this.sessionUUID,
                                        data: sanitizedInput,
                                        conditions: this.conditions[this.sessionUUID],
                                        systemID: "1"
                                    })
                                })
                                .then((response) => {
                                    if (!response.ok) {
                                        throw new Error(response.error)
                                    }
                                    return response.json();
                                })
                              response.intent_id = this.responseApi.intent_id
                              this.addBotMessage(response);
                            } catch (error) {
                              this.responseApi = {}
                              this.showFeedbackButtons = true
                            }
                          }
                        //OVDJE SE SAD SPREMA VRIJEDNOST U TABLICU LOGOVA
                    } else if (this.responseApi.response_type === 'Regularni izraz') {
                        // Handle "Regularni izraz" user response here
                        var regEx = new RegExp(this.responseApi.customer_response.split(' ')[1]);
                        if (regEx.test(sanitizedInput)) {
                            if (this.responseApi.continuation === 'Vrati se na pod-akciju') {
                                let response = await fetch('http://172.20.67.24:8081/goToStep?intent_id=' + this.responseApi.intent_id + '&system_id=1' + '&id=' + this.responseApi.previous_response.id, {
                                        method: 'GET',
                                    })
                                    .then(response => {
                                        if (!response.ok) {
                                            throw new Error(response.error);
                                        }
                                        return response.json();
                                    })
                                    .then(data => JSON.parse(data)[0]);
                                response.intent_id = this.responseApi.intent_id
                                this.selectedFeedbackButton = false;
                                this.addBotMessage(response)
                            } else if (this.responseApi.continuation === 'Nastavite na idući korak') {
                                let condition = {
                                    subject: this.responseApi.assistant_answer,
                                    predicate: 'je',
                                    object: "defined",
                                }
                                // Push the condition into the session's conditions array
                                this.conditions[this.sessionUUID].push(condition);
                                const response = await fetch('http://172.20.67.24:8081/userResponse', {
                                        method: "POST",
                                        headers: {
                                            'Accept': 'application/json',
                                            'Content-Type': 'application/json'
                                        },
                                        body: JSON.stringify({
                                            conditions: this.conditions[this.sessionUUID],
                                            intent_id: this.responseApi.intent_id,
                                            id: this.responseApi.position,
                                            uuid: this.sessionUUID,
                                            systemID: "1",
                                            answer: sanitizedInput
                                        })
                                    })
                                    .then((response) => {
                                        if (!response.ok) {
                                            throw new Error(response.error)
                                        }
                                        return response.json();
                                    })
                                response.intent_id = this.responseApi.intent_id
                                this.addBotMessage(response);
                            } else if (this.responseApi.continuation === 'Završetak radnje') {
                                this.responseApi = {}
                                this.showFeedbackButtons = true
                            }
                            else if(this.responseApi.continuation === 'Kontaktirajte agenta'){
                                try {
                                  let condition = {
                                    subject: this.responseApi.assistant_answer,
                                    predicate: 'je',
                                    object: "defined",
                                  }
                                  // Push the condition into the session's conditions array
                                  this.conditions[this.sessionUUID].push(condition);
            
                                  const response = await fetch('http://172.20.67.24:8081/sendMail', {
                                    method: "POST",
                                    headers: {
                                        'Accept': 'application/json',
                                        'Content-Type': 'application/json'
                                    },
                                    body: JSON.stringify({
                                        response: this.responseApi,
                                        session_id: this.sessionUUID,
                                        data: sanitizedInput,
                                        conditions: this.conditions[this.sessionUUID],
                                        systemID: "1"
                                    })
                                    })
                                    .then((response) => {
                                        if (!response.ok) {
                                            throw new Error(response.error)
                                        }
                                        return response.json();
                                    })
                                  response.intent_id = this.responseApi.intent_id
                                  this.addBotMessage(response);
                                } catch (error) {
                                  this.responseApi = {}
                                  this.showFeedbackButtons = true
                                }
                              }
                            //OVDJE SE SAD SPREMA VRIJEDNOST U TABLICU LOGOVA
                        } else {
                            const errorMessage = "Unijeli ste netočan regularni izraz. Molim Vas pokušajte ponovno.";
                            let messageText = `<div class="bot-response text" text-first="true">` + errorMessage + '</div>'
                            this.messages.push({
                                text: '<svg style="height:15px;width:20px" version="1.1" id="svg1" width="468" height="429.33334" viewBox="0 0 468 429.33334" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg"> <defs id="defs1" /> <g id="g1"> <image width="468" height="429.33334" preserveAspectRatio="none" xlink:href="data:image/png;base64,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&#10;" id="image1" /> </g></svg></div><span>Virtualni asistent</span>',
                              classes: ['captionBot', 'msgCaption'],
                              dataUser: false,
                            },
                            {
                              text: messageText,
                              classes: ['message'],
                              dataUser: false});
                            }
                    } else {
                        // For other response types, use the default DataService.sendMessage
                        const response = await fetch('http://172.20.67.24:8081/chatbotSentMessage', {
                                method: "POST",
                                headers: {
                                    'Accept': 'application/json',
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify({
                                    question: sanitizedInput,
                                    systemID: "1",
                                    uuid: this.sessionUUID
                                })
                            })
                            .then((response) => {
                                if (!response.ok) {
                                    throw new Error(response.error)
                                }
                                return response.json();
                            })
                        this.conditions[this.sessionUUID] = []
                        if (response.intent_id) {
                            this.selectedFeedbackButton = false;
                            this.intent_id = response.intent_id
                            this.addBotMessage(response);
                        } else if (Array.isArray(response)) {
                            this.addPossibleIntents(response)
                        } else {
                            this.addBotMessage({
                                assistant_answer: response
                            });
                        }
                    }
                    // Clear the input field after sending the message.
                    this.inputValue = '';
                    this.$refs.textarea.style.height = '44px'
                    this.scrollChatToBottom();
                } catch (error) {
                    console.error('Error sending message:', error);
                }
            }
        },

        addUserMessage(message) {
            this.messages.push({
                text: `<div class="captionUser">Vi</div>`,
                classes: ['message', 'msgCaption'],
                dataUser: true,
            });
            this.messages.push({
                text: `<div class="user-response">${message}</div>`,
                classes: ['message'],
                dataUser: true,
            });
            this.scrollChatToBottom()
        },

        async addBotMessage(message) {
            this.responseApi = message
            this.messages.push({
                text: '<svg style="height:15px;width:20px" version="1.1" id="svg1" width="468" height="429.33334" viewBox="0 0 468 429.33334" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg"> <defs id="defs1" /> <g id="g1"> <image width="468" height="429.33334" preserveAspectRatio="none" xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAV8AAAFCCAYAAABW/d7EAAAAAXNSR0IArs4c6QAAAARnQU1BAACx&#10;jwv8YQUAAAAJcEhZcwAACxEAAAsRAX9kX5EAAAAhdEVYdENyZWF0aW9uIFRpbWUAMjAyMjoxMTow&#10;NCAxMDowNDo1NwsWYUAAAAeWSURBVHhe7dwxjytXGYBhz82fQAJEGqgoKEKZLi0VoqDjFwASDRV0&#10;6HZJk5qKgKCgRVQpKfgp9FRZc854xtd3g9LZr737PLrOjJ1I451vzruz3qss//332+MBgCtbxmPk&#10;dhnbufnPn34ovgA3sQf4cHhzegGA69rCO7djI74AVzWjO+0fMpwCLL4A17J2d4vu3uDVUXwBrma/&#10;2Z2pPe+fiC/AVc1b3qfT7tzf7oDFF+CqLj92GPvbU/EFuIX9Ywd3vgA3sMX2ZDxZI+xvOwBc137H&#10;+16F/W0HgBuaJV7WDIsvwLWsN7vzH/Mxwjv/vw7T2C7H49P5phiAaxiZPc74bve7Y9+dL8BVzfCO&#10;zUV4552v+AJc1bL+Ods+ehBfgKu7rO+J+AIExBcgIL4AAfEFCIgvQEB8AQLiCxAQX4CA+AIExBcg&#10;IL4AAfEFCIgvQEB8AQLiCxAQX4CA+AIExBcgIL4AAfEFCIgvQEB8AQLiCxAQX4CA+AIExBcgIL4A&#10;AfEFCIgvQEB8AQLiCxAQX4CA+AIExBcgIL4AAfEFCIgvQEB8AQLiCxB4AfE9bpuxnY/L57dwPu5u&#10;37/R8R/KHZ6TfXbnGZrfXXm+jp8/f2DL8fj02F/N8Wl8FeN7yBzKMl9Yxu7xsCzL4aMf/3T9T65q&#10;HOe9C+L8fDl8/8PvHP78t89Or792+5w2x6enwx9+//nh7//4cnul8fZ3vzp88pOPx96Y23hPhzcX&#10;9yPrNbVeVK/WTdbQN/jBh989fPHXTy/W1TMPPJ/Hv/PdF/Q6hNOAZnjX7enfXNd5gb472np8d06b&#10;cR7WRbOdk20BLSNy85tk7bjOaby38xynd++T1jqF81yGff/ipUf1+PGd5kLZH7sxpOOtBjSOe74m&#10;xv7XLphXbZyH/Vzs49nndAfn6M3+U9OF9YfB+d7M8H7MGS3jcZ7V48/nZcT3vFAuF9Ec1LZ7de8u&#10;gvWQ8wJ5tqBfvfNCmedlOzd3cI7Od9/na2hu3s2TO7DP6Gk81jmdnj66x4/vHrr5meL+3XAd1u2G&#10;NO6x10U8F+3lwt0uGYbjV1+dZrN+TDRntM0r9ma+hXVmY4bzM9957ZyvIe7KNqd3189jexF3vusy&#10;2WZyWjzzhbm/ba/sOC6KGd0Z4PVOajv+/jZetS1iywcfnPdXa4RvNKBvcH5Lc2zzl21zXa8zNL27&#10;MuexzmQOaIT34pe3j+oFxHf7BdtcOHMhXQxo7l3fPNb4cxmW+ZrFezLPw35u9nNyR6dm/b3As9md&#10;fnq5fI3c5YxeQHinx/8qLgdxGbzx+m2WzzzKsyPNC+W9Bf3Kfe0b0T3Vdzzm+7vn9/ja/d/5PL6X&#10;8S0E4MGIL0BAfAEC4gsQEF+AgPgCBMQXICC+AAHxBQiIL0BAfAEC4gsQEF+AgPgCBMQXICC+AAHx&#10;BQiIL0BAfAEC4gsQEF+AgPgCBMQXICC+AAHxBQiIL0BAfAEC4gsQEF+AgPgCBMQXICC+AAHxBQiI&#10;L0BAfAEC4gsQEF+AgPgCBMQXICC+AAHxBQiIL0BAfAEC4gsQEF+AgPgCBMQXICC+AAHxBQiIL0BA&#10;fAEC4gsQEF+AgPgCBMQXICC+AAHxBQiIL0BAfAEC4gsQEF+AgPgCBMQXICC+AAHxBQiIL0BAfAEC&#10;4gsQEF+AgPgCBMQXICC+AAHxBQiIL0BAfAEC4gsQEF+AgPgCBMQXICC+AAHxBQiIL0BAfAEC4gsQ&#10;EF+AgPgCBMQXICC+AAHxBQiIL0BAfAEC4gsQEF+AgPgCBMQXICC+AAHxBQiIL0BAfAEC4gsQEF+A&#10;gPgCBMQXICC+AAHxBQiIL0BAfAEC4gsQEF+AgPgCBMQXICC+AAHxBQiIL0BAfAEC4gsQEF+AgPgC&#10;BMQXICC+AAHxBQiIL0BAfAEC4gsQEF+AgPgCBMQXICC+AAHxBQiIL0BAfAEC4gsQEF+AgPgCBMQX&#10;ICC+AAHxBQiIL0BAfAEC4gsQEF+AgPgCBMQXICC+AAHxBQiIL0BAfAEC4gsQEF+AgPgCBMQXICC+&#10;AAHxBQiIL0BAfAEC4gsQEF+AgPgCBMQXICC+AAHxBQiIL0BAfAEC4gsQEF+AgPgCBMQXICC+AAHx&#10;BQiIL0BAfAEC4gsQEF+AgPgCBMQXICC+AAHxBQiIL0BAfAEC4gsQEF+AgPgCBMQXICC+AAHxBQiI&#10;L0BAfAEC4gsQEF+AgPgCBMQXICC+AAHxBQiIL0BAfAEC4gsQEF+AgPgCBMQXICC+AAHxBQiIL0BA&#10;fAEC4gsQEF+AgPgCBMQXICC+AAHxBQiIL0BAfAEC4gsQEF+AgPgCBMQXICC+AAHxBQiIL0BAfAEC&#10;4gsQEF+AgPgCBMQXICC+AAHxBQiIL0BAfAEC4gsQEF+AgPgCBMQXICC+AAHxBQiIL0BAfAEC4gsQ&#10;EF+AgPgCBMQXICC+AAHxBQiIL0BAfAEC4gsQEF+AgPgCBMQXICC+AAHxBQiIL0BAfAEC4gsQEF+A&#10;gPgCBMQXILAcj0/Hbf9lOI4vZ1nW3Z//7NfrtvK9b3/r8Paz327PeO6Pn//l8M8v/7U9a/zml784&#10;fPTxj7Znw8X1gzV0TS8vvgB373D4H83MEo9SQIIhAAAAAElFTkSuQmCC&#10;" id="image1" /> </g></svg></div><span>Virtualni asistent</span>',            
                classes: ['captionBot', 'msgCaption'],
        	    dataUser: false,
      	   });


            let messageText = `<div class="bot-response text" text-first="true"><pre>` + message.assistant_answer + `</pre></div><p class="time-text">` + new Date().toLocaleTimeString('en-US', { hour12: false }) + `</p>`
            let tmp = message.assistant_answer
            message.assistant_answer = tmp

            if (!message.assistant_answer.includes("timer-content")) {
                this.messages.push({
                    text: messageText,
                    classes: ['message'],
                    dataUser: false,
                });
            } else {
                this.messages.push({
                    text: `<div class="bot-response text" text-first="true"><pre></pre></div>`,
                    classes: ['message'],
                    dataUser: false,
                });
                await this.displayContentWithDelays(message);
                this.messages[this.messages.length - 1].text += '<p class="time-text">' + new Date().toLocaleTimeString('en-US', { hour12: false }) + `</p>`
            }


            /*MAIN LOGIC FOR CHATBOT*/
            if (message.response_type === 'Opcije') {
                // Display the options as buttons.
                this.showOptions = true; // Show chatbot options
                this.chatbotOptions = this.renderOptions(message);
            } else if (message.response_type === 'Regularni izraz' || message.response_type === 'Slobodni tekst') {
                console.log()
            } else if (message.continuation === 'Vrati se na pod-akciju') {
                let response = await fetch('http://172.20.67.24:8081/goToStep?intent_id=' + this.responseApi.intent_id + '&system_id=1' + '&id=' + this.responseApi.previous_response.id, {
                        method: 'GET',
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(response.error);
                        }
                        return response.json();
                    })
                    .then(data => JSON.parse(data)[0]);
                response.intent_id = message.intent_id
                this.selectedFeedbackButton = false;
                this.addBotMessage(response)
            } else if (message.continuation === 'Nastavite na idući korak') {
                try {
                    const response = await fetch('http://172.20.67.24:8081/nextStep', {
                            method: "POST",
                            headers: {
                                'Accept': 'application/json',
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                response: message,
                                conditions: this.conditions[this.sessionUUID],
                                system_id: "1",
                            })
                        })
                        .then((response) => {
                            if (!response.ok) {
                                throw new Error(response.error)
                            }
                            return response.json();
                        })
                    response.intent_id = message.intent_id
                    this.showOptions = false
                    this.chatbotOptions = ''
                    this.addBotMessage(response);
                } catch (error) {
                    this.responseApi = {}
                    this.showFeedbackButtons = true
                }
            } else if (message.continuation === 'Završetak radnje') {
                this.responseApi = {}
                this.showFeedbackButtons = true
            }
            else if(message.continuation === 'Kontaktirajte agenta'){
                try {
                    const response = await fetch('http://172.20.67.24:8081/sendMail', {
                        method: "POST",
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            response: this.responseApi,
                            session_id: this.sessionUUID,
                            data: '',
                            conditions: this.conditions[this.sessionUUID],
                            systemID: "1"
                        })
                    })
                    .then((response) => {
                        if (!response.ok) {
                            throw new Error(response.error)
                        }
                        return response.json();
                    })
                  response.intent_id = this.responseApi.intent_id
                  this.addBotMessage(response);
                } catch (error) {
                  this.responseApi = {}
                  this.showFeedbackButtons = true
                }
              }


            this.scrollChatToBottom();
        },

        addPossibleIntents(message) {
            this.messages.push({
                text: '<svg style="height:15px;width:20px" version="1.1" id="svg1" width="468" height="429.33334" viewBox="0 0 468 429.33334" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg"> <defs id="defs1" /> <g id="g1"> <image width="468" height="429.33334" preserveAspectRatio="none" xlink:href="data:image/png;base64,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&#10;" id="image1" /> </g></svg></div><span>Virtualni asistent</span>',
                classes: ['captionBot', 'msgCaption'],
        	    dataUser: false,
      	   });
             let messageText = `<div class="bot-response text" text-first="true"> Molim Vas odaberite temu na koju biste htjeli odgovor <br> <div style="display:grid">`;
             let counter = 0;
             message.forEach((option) => {
               counter++;
               (option.intent_name == 'PRETRAŽI BAZU ZNANJA' || option.intent_name == 'PREFORMULIRAT ĆU PITANJE') ? messageText += "<p style='text-align:center'>ili</p>" : ''
               messageText += `<button class="bot-option" data-intent-id="${option.intent_id}" data-text="${option.intent_name}" data-question="${option.question}" data-threshold="${option.threshold}">${option.intent_name.toUpperCase()}</button>`;
             });
             messageText += '</div></div><p class="time-text">' + new Date().toLocaleTimeString('en-US', { hour12: false }); + `</p>`
             this.messages.push({
               text: messageText,
               classes: ['message'],
               dataUser: false,
             });
            this.scrollChatToBottom();
        },

        renderOptions(message) {
            // Clone the message object to avoid modifying the original data
            const modifiedMessage = { ...message };
        
            // Replace img elements with "SLIKA"
            const container = document.createElement('div');
            container.innerHTML = modifiedMessage.assistant_answer;
            
            container.querySelectorAll('img').forEach((img) => {
                img.replaceWith(document.createTextNode(''));
            });
        
            // Replace pause elements with "PAUSE {duration}s"
            container.querySelectorAll('.timer-content').forEach((div) => {
                div.replaceWith(document.createTextNode(''));
            });
        
            // Update the modified message with the replaced HTML
            modifiedMessage.assistant_answer = container.innerHTML;
        
            // Generate HTML for options using the modified message
            let optionsHtml = '';
            modifiedMessage.customer_response.forEach((option) => {
                optionsHtml += `<button class="bot-option" data-text='${modifiedMessage.assistant_answer}'>${option}</button>`;
            });
        
            // Remove extra white spaces from the generated HTML
            return optionsHtml;
        },

        async handleUserResponse(selectedOption, text) {
            this.addUserMessage(selectedOption)
            try {
                // Iterate through all options to build conditions
                this.responseApi.customer_response.forEach((option) => {
                    const conditionLog = {
                        subject: text,
                        predicate: option === selectedOption ? 'je' : 'nije', // Condition based on selection
                        object: option,
                    };
                    // Add the condition log to the array
                    this.conditions[this.sessionUUID].push(conditionLog);
                });

                // Make an API call to send the user's selected option.
                const response = await fetch('http://172.20.67.24:8081/chatbotUserResponse', {
                        method: "POST",
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            conditions: this.conditions[this.sessionUUID],
                            intent_id: this.responseApi.intent_id,
                            id: this.responseApi.position,
                            uuid: this.sessionUUID,
                            systemID: "1",
                            answer: selectedOption
                        })
                    })
                    .then((response) => {
                        if (!response.ok) {
                            throw new Error(response.error)
                        }
                        return response.json();
                    })
                response.intent_id = this.responseApi.intent_id
                this.responseApi = response
                this.showOptions = false
                this.chatbotOptions = ''
                // Update the chat interface with the bot's response.
                this.addBotMessage(response);
            } catch (error) {
                console.error('Error handling user response:', error);
            }
        },

        scrollChatToBottom() {
            this.$nextTick(() => {
                // Use this.$refs to access the chat container element
                const chatContainer = this.$refs.chatContainer;

                if (chatContainer) {
                    // Check if chatContainer is defined
                    chatContainer.scrollTop = chatContainer.scrollHeight;                }
            });
        },

        async handleFeedback(value) {
            try {
                if (value) {
                    await fetch('http://172.20.67.24:8081/thumbsUp?uuid=' + this.sessionUUID + '&system_id=' + "1" + '&intent_id=' + this.intent_id, {
                            method: 'GET',
                        })
                        .then((response) => {
                            if (!response.ok) {
                                throw new Error(response.error)
                            }
                            return response.json();
                        })
                    this.selectedFeedbackButton = 'up'
                } else {
                    await fetch('http://172.20.67.24:8081/thumbsDown?uuid=' + this.sessionUUID + '&system_id=' + "1" + '&intent_id=' + this.intent_id, {
                            method: 'GET',
                        })
                        .then((response) => {
                            if (!response.ok) {
                                throw new Error(response.error)
                            }
                            return response.json();
                        })
                    this.selectedFeedbackButton = 'down'
                }
            } catch (error) {
                console.error(error);
            }
        },


        /*ONLY IF CONTENT INCLUDES PAUSE*/
        async displayContentWithDelays(message) {
            const tempElement = document.createElement("div");
            tempElement.innerHTML = message.assistant_answer;
      
            const messageContentElement = document.createElement("div");
      
            const processNode = async (node, isFirstNode, isLastNode) => {
              if (node.nodeType === Node.TEXT_NODE) {
                let textNode = document.createTextNode(node.textContent.trim());
      
                // Handle text formatting
                const formattingTags = ["B", "I"];
                let parent = node.parentNode;
                while (parent) {
                  if (formattingTags.includes(parent.nodeName)) {
                    const formattedNode = document.createElement(parent.nodeName);
                    formattedNode.appendChild(textNode);
                    textNode = formattedNode;
                  }
                  parent = parent.parentNode;
                }
      
                messageContentElement.appendChild(textNode);
              } else if (node.nodeType === Node.ELEMENT_NODE) {
                if (node.nodeName === "A") {
                  const link = document.createElement("a");
                  link.href = node.getAttribute("href");
                  link.textContent = node.textContent;
                  messageContentElement.appendChild(link);
                } else if (node.nodeName === "IMG") {
                  const image = document.createElement("img");
                  image.src = node.getAttribute("src");
                  image.alt = node.getAttribute("alt");
                  messageContentElement.appendChild(image);
                } else if (node.nodeName === "BR" && !isFirstNode) {
                  messageContentElement.appendChild(document.createElement("br"));
                } else if (node.classList.contains("timer-content")) {
                  const duration = parseFloat(
                    node.querySelector("p").getAttribute("data-duration")
                  );
                  if (!isNaN(duration) && duration > 0) {
                    // Append the content before the pause to the message content element
                    if (this.messages.length > 0) {
                      this.messages[this.messages.length - 1].text =
                        this.removeLastOccurrence(
                          this.messages[this.messages.length - 1].text,
                          messageContentElement.innerHTML
                        );
                      this.messages[this.messages.length - 1].text =
                        this.removeLastOccurrence(
                          this.messages[this.messages.length - 1].text,
                          `<div><h1 class="dot one">.</h1><h1 class="dot two">.</h1><h1 class="dot three">.</h1></div>`
                        );
                    }
                    messageContentElement.innerHTML = "";
                    // Delay here
                    this.scrollChatToBottom();
                    await new Promise((resolve) =>
                      setTimeout(resolve, duration * 1000)
                    );
                  }
                  this.messages[this.messages.length - 1].text = this.messages[
                    this.messages.length - 1
                  ].text.replace(
                    `<div><h1 class="dot one">.</h1><h1 class="dot two">.</h1><h1 class="dot three">.</h1></div>`,
                    ""
                  );
                  !isFirstNode
                    ? messageContentElement.appendChild(document.createElement("br"))
                    : "";
                } else {
                  const childNodes = node.childNodes;
                  for (let i = 0; i < childNodes.length; i++) {
                    const childNode = childNodes[i];
                    await processNode(
                      childNode,
                      isFirstNode && i === 0,
                      isLastNode && i === childNodes.length - 1
                    );
                  }
                }
              }
            };
      
            const childNodes = tempElement.childNodes;
            for (let i = 0; i < childNodes.length; i++) {
              const childNode = childNodes[i];
              await processNode(
                childNode,
                i === 0 ||
                  (i === 1 &&
                    (childNodes[0].textContent.trim().length === 0 ||
                      childNodes[0].nodeName === "BR")),
                i === childNodes.length - 1
              ); //additional conditions because blank spaces in the beggining or empty <br>
            }
      
            if (this.messages.length > 0) {
              this.messages[this.messages.length - 1].text =
                this.removeLastOccurrence(
                  this.messages[this.messages.length - 1].text,
                  messageContentElement.innerHTML
                );
            }
          },
      
          removeLastOccurrence(inputString, update) {
            const lastIndex = inputString.lastIndexOf('</pre></div>');
            const beforeSubstring = inputString.slice(0, lastIndex);
            const afterSubstring = inputString.slice(lastIndex + '</pre></div>'.length);
            return beforeSubstring + afterSubstring + update + '</pre></div>';
          },

        toggleMinimized() {
            this.minimized = !this.minimized;
        },

        refresh() {
            this.messages = []; // Clear messages
            this.responseApi = {}; // Reset responseApi
            this.showFeedbackButtons = false; // Reset feedback buttons
            this.showOptions = false;
            this.chatbotOptions = ''
            this.initializeBot(); // Restart the chatbot
        },
        adjustTextareaHeight() {
            const textarea = this.$refs.textarea;
            textarea.style.height = 'auto';
            textarea.style.height = `${textarea.scrollHeight}px`;
        },
        async changeVisibility(){
            if(this.showChatbot){
                this.showStars = true;
            }
            else{
                this.showChatbot = true
                let res = await fetch('http://172.20.67.24:8081/getInitialChat?system_id=1', {
                        method: 'GET',
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(response.error);
                        }
                        return response.json();
                    })
                this.system_initial = res[0].system_initial
                // Generate a session UUID when the component is mounted

                this.sessionUUID = uuidv4();
                this.conditions[this.sessionUUID] = [];
            
                // Automatically send an initial message from the bot
                this.initializeBot();
            }
        },
        async sendStarsFeedback(){
            await fetch('http://172.20.67.24:8081/feedbackResponse', {
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    stars: this.selectedStars,
                    comment: this.comment
                })
            })
            .then((response) => {
                if (!response.ok) {
                    throw new Error(response.error)
                }
                return response.json();
            })
            // Process feedback submission here
            console.log("Stars:", this.selectedStars);
            console.log("Comment:", this.comment);
            // Reset modal state after submission
            this.showChatbot = false;
            this.showStars = false;
            this.selectedStars = 0;
            this.comment = "";
            this.messages = [];
            this.showFeedbackButtons = false;
        },
        closeFeedBack(){
            // Reset modal state after submission
            this.showChatbot = false;
            this.showStars = false;
            this.selectedStars = 0;
            this.comment = "";
            this.messages = [];
            this.showFeedbackButtons = false;
        }
    },
};
