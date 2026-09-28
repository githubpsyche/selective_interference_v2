-- Present the imported Word title page using Quarto's native manuscript template.
-- The authoring QMD and frozen reference are not modified. Run after quarto-review
-- so review boundaries travel with their text into the rendered title block.
function Pandoc(doc)
  if not quarto.doc.is_format("html") or not doc.meta["review-import-front-matter"] then
    return nil
  end
  local blocks = doc.blocks
  local abstract_index, introduction_index, note_index, keywords_index
  for i, block in ipairs(blocks) do
    local text = pandoc.utils.stringify(block)
    if block.t == "Header" then
      if text == "Author Note" then note_index = i end
      if text == "Abstract" then abstract_index = i end
      if text == "Introduction" then introduction_index = i; break end
    elseif block.t == "Para" and text:match("^Keywords:") then
      keywords_index = i
    end
  end
  if not (blocks[1].t == "Header" and blocks[2].t == "Para"
      and blocks[3].t == "Para" and keywords_index
      and abstract_index and introduction_index) then
    error("The imported title-page structure has changed; update manuscript-frontmatter.lua before rendering.")
  end
  local function opens_deleted_note(block)
    if block.t ~= "Para" or pandoc.utils.stringify(block) ~= "" then return false end
    local starts, ends = false, false
    block:walk({RawInline = function(inline)
      if inline.format ~= "html" or not inline.text:find('data-review-kind="D"', 1, true) then return end
      if inline.text:find('data-review-edge="S"', 1, true) then starts = true end
      if inline.text:find('data-review-edge="E"', 1, true) then ends = true end
    end})
    return starts and not ends
  end
  -- The automatic deletion of Author Note begins in an annotation-only
  -- paragraph before its heading. Move that opening boundary with the note;
  -- leaving it on the affiliation would mark the intervening abstract deleted.
  local note_start_index = note_index or keywords_index
  if note_index and note_index > 4 and opens_deleted_note(blocks[note_index - 1]) then
    note_start_index = note_index - 1
  end
  local title = blocks[1].content
  local affiliation = pandoc.Inlines(blocks[3].content)
  -- Word's empty formatting revisions still need one rendered anchor each.
  for i = 4, note_start_index - 1 do
    if blocks[i].t ~= "Para" then error("Unexpected imported title-page block") end
    if pandoc.utils.stringify(blocks[i]) ~= "" then
      affiliation:insert(pandoc.LineBreak())
    end
    affiliation:extend(blocks[i].content)
  end
  doc.meta.title = pandoc.MetaInlines(title)
  -- Keep Quarto's five structured authors for its native manuscript title
  -- metadata. The imported Word author line is one review range, so it cannot
  -- be split into five template rows without breaking that range. Present it
  -- separately while review is visible; Reading view uses the native rows.
  doc.meta["review-frontmatter"] = pandoc.MetaBlocks({
    pandoc.Div({
      pandoc.Div({pandoc.Plain({pandoc.Str("Authors")})}, pandoc.Attr("", {"quarto-title-meta-heading"})),
      pandoc.Para(blocks[2].content),
      pandoc.Div({pandoc.Plain({pandoc.Str("Affiliations")})}, pandoc.Attr("", {"quarto-title-meta-heading"})),
      pandoc.Para(affiliation)
    }, pandoc.Attr("", {"qr-reviewed-frontmatter-content"}))
  })
  local keywords = pandoc.Inlines(blocks[keywords_index].content)
  -- The native template supplies the label; retain all annotated keyword text.
  keywords:remove(1)
  if keywords[1] and keywords[1].t == "Str" and keywords[1].text == ":" then keywords:remove(1) end
  if keywords[1] and keywords[1].t == "Space" then keywords:remove(1) end
  -- Pandoc also places `keywords` in an HTML attribute, where raw review
  -- boundaries would corrupt the head. Render the annotated line in the
  -- title block without turning the body Abstract into Quarto metadata.
  doc.meta["review-keywords"] = pandoc.MetaBlocks({pandoc.Para(keywords)})
  -- The project YAML continues to supply native author/affiliation metadata.
  local body = pandoc.Blocks({})
  -- An older review round may still contain the author note. The current
  -- working manuscript omits it while retaining the source review history.
  if note_index then
    for i = note_start_index, keywords_index - 1 do
      local block = blocks[i]
      if block.t == "Header" then
        block.level = 2
        block.classes:insert("unlisted")
        block.classes:insert("unnumbered")
      end
      body:insert(block)
    end
  end
  for i = keywords_index + 1, abstract_index - 1 do
    local block = blocks[i]
    local annotated = false
    block:walk({RawInline = function(inline)
      if inline.format == "html" and inline.text:find("qr-boundary", 1, true) then
        annotated = true
      end
    end})
    if annotated or block.t ~= "Header" then
      if block.t == "Header" then
        block.classes:insert("unlisted")
        block.classes:insert("unnumbered")
      end
      body:insert(pandoc.Div({block}, pandoc.Attr("", {"qr-repeated-title"})))
    end
  end
  for i = abstract_index, introduction_index - 1 do body:insert(blocks[i]) end
  for i = introduction_index, #blocks do body:insert(blocks[i]) end
  doc.blocks = body
  return doc
end
