new Vue({
    el: '#form_container',
    data() {
        return {
            mode: '1', // 模式：定时下单/有货自动下单
            date: '', // 下单时间
            area: '', // 所在地区
            skurl: '', // 商品url
            count: '1', // 购买数量
            retry: '10', // 重试次数
            work_count: '1', // 启动线程数
            timeout: '30', // 超时时间
            eid: '',
            fp: '',
            timeSelectAble: true,
            dialogVisible: false,
            dialog: '',
            skuid: '',
            qrUrl: './img/qr_code.png',
            qrVisible: false,
            qrReq: undefined,
            qrID: 0,
            qrReset: true,
            logReq: undefined,
            title: '错误',
            task: true,
        }
    },
    created() {
        let area = localStorage.getItem('area')
        if (area) {
            this.area = area
        }
        this.runningCheck()
    },
    mounted() {
        this.getEidFp()
        setTimeout(() => {
            this.main()
        }, 100)
    },
    methods: {
        main() { },

        upload() {
            if (!this.checkValid()) return
            this.storage()
            let url = '/api/jd-shopper'
            if (this.mode === '2' || this.mode === 2) {
                this.date = new Date(this.date.getTime() + 1000 * 60 * 60 * 8)
            }
            let data = {
                mode: this.mode,
                date: this.date,
                area: this.area,
                skuid: this.skuid,
                count: this.count,
                retry: this.retry,
                work_count: this.work_count,
                timeout: this.timeout,
                eid: this.eid,
                fp: this.fp,
            }
            fetch(url, {
                body: JSON.stringify(data), // must match 'Content-Type' header
                cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
                credentials: 'same-origin', // include, same-origin, *omit
                headers: {
                    'user-agent': 'Mozilla/4.0 MDN Example',
                    'content-type': 'application/json',
                },
                method: 'POST', // *GET, POST, PUT, DELETE, etc.
                mode: 'cors', // no-cors, cors, *same-origin
                redirect: 'follow', // manual, *follow, error
                referrer: 'no-referrer', // *client, no-referrer
            })
                .then(response => {
                    return response.json()
                })
                .then(res => {
                    if (res.data) {
                        this.getLog()
                        this.task = false
                    } else {
                        setTimeout(() => {
                            this.qrShow()
                            this.loginCheck()
                        }, 500)
                    }
                })
        },

        buyMode(value) {
            if (this.mode === '1' || this.mode === 1) {
                this.timeSelectAble = true
            } else {
                this.timeSelectAble = false
            }
        },

        getEidFp() {
            let that = this
            setTimeout(() => {
                try {
                    getJdEid(function (eid, fp, udfp) {
                        that.eid = eid
                        that.fp = fp
                    })
                } catch (e) {
                    that.dialogShow('获取eid与fp失败，请手动获取。')
                }
            }, 0)
        },

        reset() {
            this.mode = '1' // 模式：定时下单/有货自动下单
            this.date = ''
            this.area = '' // 所在地区
            this.skurl = '' // 商品url
            this.count = '1' // 购买数量
            this.retry = '10' // 重试次数
            this.work_count = '1' // 启动线程数
            this.timeout = '3' // 超时时间
            this.eid = ''
            this.fp = ''
            this.storage()
        },

        dialogShow(mes) {
            this.dialog = mes
            this.dialogVisible = true
        },

        checkValid() {
            if (this.area == '' || this.skurl == '') {
                this.dialogShow('地区ID与商品链接不能为空')
                return false
            } else if (this.mode == '2' && this.date == '') {
                this.dialogShow('定时下单需设置时间')
                return false
            }
            let skuid = this.skurl.match(
                new RegExp(`https://item.jd.com/(.*?).html`)
            )
            skuid = skuid ? skuid[1] : null
            if (skuid == null) {
                skuid = this.skurl.replace(/[^0-9]/gi, '')
                reNum = /^[0-9]+.?[0-9]*/
                if (!reNum.test(skuid)) {
                    this.dialogShow('请输入正确的网址')
                    return false
                }
            }
            this.skuid = skuid
            return true
        },

        qrShow() {
            this.qrVisible = true
            this.qrID = 0
            this.qrReq = setInterval(function () {
                let imgDiv = document.getElementsByClassName('el-image')[0]
                imgDiv.removeChild(imgDiv.childNodes[0])
                this.qrID++
                this.qrUrl = './img/qr_code.png'
                this.qrReset = false
            }, 3000)
        },

        runningCheck() {
            let url = './api/jd-running-status'
            fetch(url)
                .then(response => {
                    return response.json()
                })
                .then(res => {
                    if (res.data) {
                        this.getLog()
                        this.task = false
                    }
                })
        },

        loginCheck() {
            let url = './api/jd-login-status'
            let loginReq = setInterval(() => {
                let imgDiv = document.getElementsByClassName('el-image')[0]
                imgDiv.innerHTML = `<img src="./img/qr_code.png?id={this.qrID}" class="el-image__inner">`
                fetch(url)
                    .then(response => {
                        return response.json()
                    })
                    .then(res => {
                        if (res.data) {
                            this.qrVisible = false
                            clearInterval(this.qrReq)
                            clearInterval(loginReq)
                            this.getLog()
                            this.task = false
                        }
                    })
            }, 1000)
        },

        getLog() {
            let url = './api/log'
            let logger = document.getElementById('log')
            const update = data => {
                let pos = logger.scrollTop + logger.offsetHeight
                let height = logger.scrollHeight
                logger.innerHTML = data
                if ((height - pos) < 5) {
                    logger.scrollTop = logger.scrollHeight
                }
            }
            const getLog = () => {
                fetch(url)
                    .then(response => {
                        return response.json()
                    })
                    .then(res => {
                        update(res.data)
                    })
            }
            getLog()
            this.logReq = setInterval(() => {
                getLog()
            }, 3000)
        },

        stop() {
            clearInterval(this.logReq)
            let url = './api/jd-stop-running'
            fetch(url)
                .then(response => {
                    return response.json()
                })
                .then(res => {
                    this.task = true
                })
        },

        exit() {
            clearInterval(this.logReq)
            let url = './api/exit'
            fetch(url)
                .then(response => {
                    return response.json()
                })
                .then(res => {
                })
            setTimeout(() => {
                window.destroy()
                window.location.href = "about:blank"
                window.close()
            }, 500)
        },

        storage() {
            localStorage.setItem('area', this.area)
        },
    },
})
