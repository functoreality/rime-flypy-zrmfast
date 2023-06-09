local function func_translator(input, seg, env)
   local trigger = env.engine.schema.config:get_string('recognizer/patterns/func_translator') or '^af(.*)$'
   local expr, n = env.engine.context.input:gsub(trigger, '%1')
   if (n == 0) then
      return
   end
   -- 如果输入串为 `afd` 则翻译
   if (expr:sub(1,1) == "d") then
      if (expr:sub(2,2) == '2' or expr:sub(2,2) == ';') then ---- 若选择次选，直接上屏
         env.engine:commit_text(os.date("%Y年%m月%d日"))
         env.engine.context:clear()
         return
      end
      yield(Candidate("date", seg.start, seg._end, os.date("%Y-%m-%d"), "日期"))
      yield(Candidate("date", seg.start, seg._end, os.date("%Y年%m月%d日"), "日期"))
   end
end

return func_translator
