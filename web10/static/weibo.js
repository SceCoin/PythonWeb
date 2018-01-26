var timeString = function(timestamp) {
    t = new Date(timestamp * 1000)
    t = t.toLocaleTimeString()
    return t
}

var commentsTemplate = function(comments) {
    var html = ''
    for(var i = 0; i < comments.length; i++) {
        var c = comments[i]
        var t = `
            <div data-commentid=${c.id} class='comment-cell' >
                ${c.content}
                <button class="comment-delete">删除评论</button>
            </div>
        `
        html += t
    }
    return html
}

var weiboTemplate = function(weibo) {
    var content = weibo.content
    var id = weibo.id
    var comments = commentsTemplate(weibo.comments)
    var t = `
        <div class='weibo-cell' data-id=${id} data-name="test">
            <div class="weibo-content">
                [weibo]: ${content}
            </div>
            <button class="weibo-delete">删除微博</button>
            <button class="weibo-edit">更新微博</button>
            <div class="comment-list">
                ${comments}
            </div>
            <div class="comment-form">
                <input type="hidden" name="weibo_id" value="">
                <input name="content" class="comment-content">
                <br>
                <button class="comment-add">添加评论</button>
            </div>
        </div>
    `
    return t
    /*
    上面的写法在 python 中是这样的
    t = """
    <div class="weibo-cell">
        <button class="weibo-delete">删除</button>
        <span>{}</span>
    </div>
    """.format(weibo)
    */
}

var insertweibo = function(weibo) {
    var weiboCell = weiboTemplate(weibo)
    // 插入 weibo-list
    var weiboList = e('.weibo-list')
    weiboList.insertAdjacentHTML('beforeend', weiboCell)
}

var insertEditForm = function(cell, weibo) {
    var content = weibo.content
    var form = `
        <div class='weibo-edit-form'>
            <input class="weibo-edit-input" value=${content}>
            <button class='weibo-update'>更新</button>
        </div>
    `
    cell.insertAdjacentHTML('afterbegin', form)
}

var insertUpdate = function(cell, weibo){
    var content = weibo.content
    var t = `
        <div class="weibo-content">
                [weibo]: ${content}
        </div>
    `
    cell.insertAdjacentHTML('afterbegin', t)
}

var insertCommentAdd = function(cell, weibo){
    var comments = weibo.content
    var t = `
        <div class="comment-list">
                ${comments}
                <button class="comment-delete">删除评论</button>
            </div>
    `
    cell.insertAdjacentHTML('afterbegin', t)
}


var loadweibos = function() {
    // 调用 ajax api 来载入数据
    apiWeiboAll(function(r) {
        // console.log('load all', r)
        // 解析为 数组
        var weibos = JSON.parse(r)
        // 循环添加到页面中
        for(var i = 0; i < weibos.length; i++) {
            var weibo = weibos[i]
            insertweibo(weibo)
        }
    })
}

var bindEventweiboAdd = function() {
    var b = e('#id-button-add-weibo')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function(){
        var input = e('#id-input-weibo')
        var content = input.value
        log('click add', content)
        var form = {
            'content': content,
        }
        apiWeiboAdd(form, function(r) {
            // 收到返回的数据, 插入到页面中
            var weibo = JSON.parse(r)
            insertweibo(weibo)
        })
    })
}

var bindEventweiboDelete = function() {
    var weiboList = e('.weibo-list')
    // 注意, 第二个参数可以直接给出定义函数
    weiboList.addEventListener('click', function(event){
        var self = event.target
        if(self.classList.contains('weibo-delete')){
            // 删除这个 weibo
            var weiboCell = self.parentElement
            var weibo_id = weiboCell.dataset.id
            // log('weibo_id----', weibo_id)
            // log('dataset---', weiboCell.dataset)
            apiWeiboDelete(weibo_id, function(r){
                log('删除成功', weibo_id)
                weiboCell.remove()
            })
        }
    })
}

var bindEventweiboEdit = function() {
    var weiboList = e('.weibo-list')
    // 注意, 第二个参数可以直接给出定义函数
    weiboList.addEventListener('click', function(event){
        var self = event.target
        if(self.classList.contains('weibo-edit')){
            var weiboCell = self.parentElement
            var content = weiboCell.children[0]
            var weibo_id = weiboCell.dataset.id

            apiWeiboAll(function(r) {
            var weibos = JSON.parse(r)
            // 循环添加到页面中
            for(var i = 0; i < weibos.length; i++) {
                var weibo = weibos[i]
                log('weibo', weibo)
                if (weibo.id == weibo_id){
                    insertEditForm(weiboCell, weibo)
                    content.remove()
                }
        }
    })
        }
    })
}


var bindEventweiboUpdate = function() {
    var weiboList = e('.weibo-list')
    // 注意, 第二个参数可以直接给出定义函数
    weiboList.addEventListener('click', function(event){
        var self = event.target
        log('self',self)
        if(self.classList.contains('weibo-update')){
            log('点击了 update ')
            //
            var editForm = self.parentElement
            // querySelector 是 DOM 元素的方法
            // document.querySelector 中的 document 是所有元素的祖先元素
            var input = editForm.querySelector('.weibo-edit-input')
            var content = input.value
            // 用 closest 方法可以找到最近的直系父节点
            var weiboCell = self.closest('.weibo-cell')
            var weibo_id = weiboCell.dataset.id
            var form = {
                'id': weibo_id,
                'content': content,
            }
            apiWeiboUpdate(form, function(r){
                log('更新成功', weibo_id)
                var weibo = JSON.parse(r)
                var selector = '[data-id="' + weibo.id + '"]'
                var weiboCell = e(selector)

                var edit = weiboCell.children[0]
                edit.remove()

                insertUpdate(weiboCell, weibo)

            })
        }
    })
}


var bindEventCommentAdd = function() {
    var weiboList = e('.weibo-list')
    // 注意, 第二个参数可以直接给出定义函数
    weiboList.addEventListener('click', function(event){
        var self = event.target
        if(self.classList.contains('comment-add')){
            log('点击了添加评论')
            var commentform = self.parentElement
            var weiboCell = self.closest('.weibo-cell')
            var weibo_id = weiboCell.dataset.id
            var input = commentform.querySelector('.comment-content')
            var content = input.value
            log('click add', content)
            var form = {
                'content': content,
                'weibo_id': weibo_id,
            }
            apiCommentAdd(form, function(r) {
                // 收到返回的数据, 插入到页面中
                var comment = JSON.parse(r)
                var selector = '[data-id="' + comment.weibo_id + '"]'
                var weiboCell = e(selector)
                var commentlist = weiboCell.children[3]

                insertCommentAdd(commentlist, comment)

            })
        }
    })
}


var bindEventCommentDelete = function() {
    var weiboList = e('.weibo-list')
    // 注意, 第二个参数可以直接给出定义函数
    weiboList.addEventListener('click', function(event){
        var self = event.target
        if(self.classList.contains('comment-delete')){
            var commentcell = self.parentElement
            var comment_id = commentcell.dataset.commentid
            // log('weibo_id----', weibo_id)
            // log('dataset---', weiboCell.dataset)
            apiCommentDelete(comment_id, function(r){
                log('删除成功', comment_id)
                commentcell.remove()
            })
        }
    })
}


var bindEvents = function() {
    bindEventweiboAdd()
    bindEventweiboDelete()
    bindEventweiboEdit()
    bindEventweiboUpdate()
    bindEventCommentAdd()
    bindEventCommentDelete()
}

var __main = function() {
    bindEvents()
    loadweibos()
}

__main()

//
// # 作业1
// # 以上课板书为基础，实现以下功能
// #
// #
// # 添加 weibo
// # 目前添加 weibo 功能并不能直接使用，程序这部分有一个小 bug，直接修复就可以了
// #
// # 作业2
// # 删除 weibo
// # 在 WeiboTemplate 函数中里补上 delete 部分，这样就可以通过事件委托实现，点击的时候发送 delete 请求。
// # 为了方便，删除 weibo 的 api 继续写在 api_todo.py 中，并且参照todo部分实现删除 weibo 功能
// #
// # 作业3
// # 更新 weibo
// # 更新主要分为三步
// # 3.1 点击 edit 按钮，隐藏当前显示的 weibo 内容，插入一个表单，里面有 weibo 内容和 update 按钮
// # 3.2 点击 update 按钮，发送 update 请求
// # 3.3 在 apt_todo 中添加 update_weibo 路由，并且参照todo部分实现更新 weibo 功能
// #
// # 作业4
// # 添加 comment
// # 绑定 comment-add 的事件，点击之后发送请求
// # 添加 add_comment 路由，并且参照todo实现增加的功能，这里需要注意 comment 是通过 weibo_id 与 weibo 关联在一起的
// #
// # 作业5
// # 删除 comment
// # WeiboTemplate 函数中需要补上 comment-delete 按钮，然后绑定响应的事件，点击之后发送请求
// # 添加 delete_comment 路由，实现删除 comment 的功能。
