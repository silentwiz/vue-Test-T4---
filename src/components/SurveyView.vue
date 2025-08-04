<script>
import { mapState } from 'pinia'
import { useSettingsStore } from '@/stores/settingsStore'

export default {
  props: {
    userName: {
      type: String,
      required: true,
    },
  },
  emits: ['show-results', 'show-login'],
  computed: {
    ...mapState(useSettingsStore, [
      'fontSize',
      'buttonColor',
      'buttonHoverColor',
      'resultColor',
      'resultHoverColor',
      'blackFont',
      'whiteFont',
    ]),
  },

  data() {
    return {
      form: {
        needSupport: '',
        specificSituation: '',
        isSocial: '',
        whoneed: '',
        precisionOrStrength: '',
        needInterfaces: '',
        interfaces: [],
        needMaintenance: '',
        whyNeedInterfaces: '',
        societalNecessity: '',
        otherComments: '',
      },
      interfaceOptions: ['脳波', '筋電', '視線', 'キーボード', 'マウス', 'その他'],
      submitted: false,
      needInt: false,
    }
  },
  methods: {
    handleSubmit() {
      const dataToSend = {
        userName: this.userName,
        ...this.form,
      }

      fetch('http://localhost:3001/api/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dataToSend),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            this.submitted = true
          } else {
            alert('送信に失敗しました')
          }
        })
        .catch(() => {
          alert('送信エラー')
        })
    },
    goToResults() {
      this.$emit('show-results')
    },
    goToLogin() {
      this.$emit('show-login')
    },
  },
}
</script>

<template>
  <div class="survey-container" :style="{ 'font-size': fontSize + 'px' }">
    <h1>{{ userName }} アンケート調査</h1>
    <form @submit.prevent="handleSubmit">
      <!-- 1. 仕事や日常生活でサポート機器が欲しいと思ったことがあるか -->
      <div class="form-group">
        <label>1. 仕事や日常生活でサポート機器が欲しいと思ったことがありますか？</label>
        <div>
          <label><input type="radio" v-model="form.needSupport" value="はい" /> はい</label>
          <label><input type="radio" v-model="form.needSupport" value="いいえ" /> いいえ</label>
        </div>
      </div>
      <div v-if="form.needSupport === 'いいえ'" class="form-group">
        <label>2-2. この技術は社会的意義があると思いますか？</label>
        <div>
          <label><input type="radio" v-model="form.isSocial" value="はい" /> はい</label>
          <label><input type="radio" v-model="form.isSocial" value="いいえ" /> いいえ</label>
        </div>
        <div v-if="form.isSocial" class="form-group">
          <label>3-2. この技術は、どのような人々の助けになると考えますか？</label>
          <textarea
            v-model="form.whoneed"
            :maxlength="100"
            rows="3"
            placeholder="例：身体に障がいのある方,高齢者,重度の神経疾患を持つ方（ALSなど）,忙しい生活を送る人（時短目的）,災害支援（がれき撤去）,その他（自由記述）"
          ></textarea>
        </div>
        <div v-if="form.whoneed.length > 0" class="form-group">
          <label>4. その他ご意見・ご要望（任意記入）</label>
          <textarea
            v-model="form.otherComments"
            rows="2"
            placeholder="ご意見・ご要望をご記入ください"
          ></textarea>
        </div>
      </div>

      <div v-if="form.needSupport === 'はい'" class="form-group">
        <div class="form-group">
          <label>2-1. 具体的にどんな場面ですか？（100文字以内）</label>
          <textarea
            v-model="form.specificSituation"
            :maxlength="100"
            rows="3"
            placeholder="例：長時間のデスクワークで手が疲れやすく、サポート機器があれば助かると感じた。"
          ></textarea>
          <div class="char-count">{{ form.specificSituation.length }}/100</div>
        </div>

        <div v-if="form.specificSituation.length > 0" class="form-group">
          <!-- 3. どの程度の精密作業又は力仕事 -->
          <div class="form-group">
            <label
              >3.
              それは、どの程度の精密作業又は力仕事ですか（どのような作業をさせたいですか）</label
            >
            <input
              type="text"
              v-model="form.precisionOrStrength"
              placeholder="例：細かい部品の組み立てなど精密な作業が必要"
            />
          </div>
        </div>

        <div v-if="form.precisionOrStrength.length > 0" class="form-group">
          <div>
            <label>4.手を使わずに操作するインターフェースは必要だと思うか）</label>
            <label><input type="radio" v-model="form.needInterfaces" value="はい" /> はい</label>
            <label
              ><input type="radio" v-model="form.needInterfaces" value="いいえ" /> いいえ</label
            >
          </div>
        </div>

        <!-- 3. どの様なインターフェースが良いか -->
        <div v-if="form.needInterfaces === 'はい'" class="form-group">
          <label>5-1. どの様なインターフェースが良いと思いますか？（複数選択可）</label>
          <div>
            <label v-for="option in interfaceOptions" :key="option">
              <input type="checkbox" :value="option" v-model="form.interfaces" />
              {{ option }}
            </label>
          </div>
        </div>

        <!-- 4. メンテナンスサポートは必要か -->
        <div
          v-if="form.needInterfaces === 'いいえ' || form.interfaces.length > 0"
          class="form-group"
        >
          <label>5-2. メンテナンスサポートは必要ですか？</label>
          <div>
            <label><input type="radio" v-model="form.needMaintenance" value="はい" /> はい</label>
            <label
              ><input type="radio" v-model="form.needMaintenance" value="いいえ" /> いいえ</label
            >
          </div>
        </div>

        <!-- 6. アンケート項目 -->
        <div v-if="form.needMaintenance" class="form-group">
          <label>6. その他ご意見・ご要望（任意記入）</label>
          <textarea
            v-model="form.otherComments"
            rows="2"
            placeholder="ご意見・ご要望をご記入ください"
          ></textarea>
        </div>
      </div>
      <button
        v-if="form.otherComments.length > 0 && submitted === false"
        type="submit"
        class="submit"
      >
        送信
      </button>
    </form>
    <button v-if="submitted" type="button" class="result-button" @click="goToLogin">戻る</button>
    <div v-if="submitted" class="success-message">ご回答ありがとうございました！</div>
  </div>
</template>

<style scoped>
.need-needmaintenance-group {
}
.need-support-group {
}
input[type='text'],
textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: var(--font-size);
}
input[type='radio'],
input[type='checkbox'] {
  margin-right: 6px;
  margin-left: 0;
  font-size: var(--font-size);
}
.survey-container {
  max-width: 29.4em;
  margin: 40px auto;
  padding: 32px 24px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.08);
  font-family: 'Microsoft YaHei', Arial, sans-serif;
}
h1 {
  text-align: center;
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 20px;
}
.form-group label {
  font-weight: bold;
  display: block;
  margin-bottom: 8px;
}
input[type='text'],
textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}
input[type='radio'],
input[type='checkbox'] {
  margin-right: 6px;
  margin-left: 0;
}

.survey-container {
  max-width: 29.4em;
  margin: 40px auto;
  padding: 32px 24px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.08);
}
h1 {
  text-align: center;
  margin-bottom: 24px;
}
h2 {
  font-size: var(--font-size);
}
.form-group {
  margin-bottom: 20px;
}
.form-group label {
  display: block;
  margin-bottom: 8px;
}
.success-message {
  color: #42b983;
  text-align: center;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #42b983;
  border-radius: 4px;
}
button {
  width: 100%;
  padding: 10px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
  color: white;
}

.submit {
  font-size: var(--font-size);
  background: v-bind(buttonColor);
  margin-top: 0.5em;
}
.submit:hover {
  font-size: var(--font-size);
  background: v-bind(buttonHoverColor);
}

.result-button {
  background: v-bind(resultColor);
  margin-top: 0.5em;
  color: v-bind(whiteFont);
  font-size: var(--font-size);
}
.result-button:hover {
  background: v-bind(resultHoverColor);
  font-size: var(--font-size);
}
</style>
