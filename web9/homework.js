/*
1. 先获取按钮的位置
2. 编写规则函数
3. 绑定到按钮上做成click事件
*/

# // 作业 1
# /*
# 实现一个登录页, 页面中有 2 个标签分别是用户名输入框和登录按钮
# 给登录按钮绑定一个 click 事件
# 检查用户名是否符合如下规则
# 1，第一位是字母
# 2，最小长度2
#
# 如果符合规则, log '检查合格'
# 如果不符合, log '用户名错误'
#
# 需要补全的代码自行解决
#
# // 作业 2
# /*
# 在上个作业的基础上
# 额外再检查用户名是否符合如下规则
# 1，只能字母或数字结尾
# 2，最大长度10
# 3，只能包含字母、数字、下划线
#
#
# 在上个作业的登录页最后增加一个 <h3></h3> 标签
# 如果符合规则 设置标签的内容为 '检查合格'
# 如果不符合, 设置标签的内容为 '用户名错误'
#
# 需要补全的代码自行解决
#
# // 作业 3
# /*
# 在上个作业的基础上
# 当检查不符合规则后, 清空用户输入的内容
# */



var log = function(){
  console.log.apply(console, arguments)
}


var template = function(tag){
  t = `
    <h3>${tag}</h3>
  `

  return t
}


var e = function(sel){
  return document.querySelector(sel)
}


var inserttag = function(tag){
  var ins = template(tag)
  var center = e('.center')
  center.insertAdjacentHTML('afterend', ins)
}


var b = e('#loginButton')
var p = e('#id-input-username')

var regs = /^[A-Z-a-z]$/
var regs2 = /^[A-Z-a-z-0-9]$/
var regs3 = /^[0-9a-zA-Z_]{1,}$/

var rules = function(){
  var h = e('h3')
  if (h){
    h.remove()
  }
  var len = p.value.length
  if (len >= 2 && len <= 10){
    if (regs.test(p.value[0]) && regs2.test(p.value[len-1])){
      if (regs3.test(p.value)){
        inserttag('检查合格')
      }else{
        inserttag('用户名错误')
        p.value = ''
      }
    }else{
        inserttag('用户名错误')
        p.value = ''
    }
  }
  else{
    inserttag('用户名错误')
    p.value = ''
  }
}

b.addEventListener('click', rules)
