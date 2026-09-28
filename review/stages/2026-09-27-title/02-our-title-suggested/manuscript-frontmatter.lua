-- Present the imported Word title page using Quarto's native manuscript template.
-- The pooled QMD and frozen reference remain unchanged. Run after quarto-review
-- so review boundaries travel with their text into the rendered front matter.
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
      and blocks[3].t == "Para" and note_index and keywords_index
      and abstract_index and introduction_index) then
    error("The imported title-page structure has changed; update manuscript-frontmatter.lua before rendering.")
  end
  local title = blocks[1].content
  local affiliation = pandoc.Inlines(blocks[3].content)
  -- Word's empty formatting revisions still need one rendered anchor each.
  for i = 4, note_index - 1 do
    if blocks[i].t ~= "Para" then error("Unexpected imported title-page block") end
    affiliation:extend(blocks[i].content)
  end
  doc.meta.title = pandoc.MetaInlines(title)
  doc.meta.authors = pandoc.MetaList({pandoc.MetaMap({
    name = pandoc.MetaInlines(blocks[2].content),
    affiliations = pandoc.MetaList({pandoc.MetaMap({name = pandoc.MetaInlines(affiliation)})})
  })})
  local keywords = pandoc.Inlines(blocks[keywords_index].content)
  -- The native template supplies the label; retain all annotated keyword text.
  keywords:remove(1)
  if keywords[1] and keywords[1].t == "Str" and keywords[1].text == ":" then keywords:remove(1) end
  if keywords[1] and keywords[1].t == "Space" then keywords:remove(1) end
  local abstract = pandoc.Blocks({})
  for i = abstract_index + 1, introduction_index - 1 do abstract:insert(blocks[i]) end
  -- Pandoc also places `keywords` in an HTML attribute, where raw review
  -- boundaries would corrupt the head. Keep the annotated keyword block with
  -- the abstract, using the manuscript template's normal presentation classes.
  doc.meta.abstract = pandoc.MetaBlocks({
    pandoc.Div(abstract, pandoc.Attr("abstract")),
    pandoc.Div({
      pandoc.Div({pandoc.Plain({pandoc.Str("Keywords")})}, pandoc.Attr("", {"block-title"})),
      pandoc.Para(keywords)
    }, pandoc.Attr("", {"keywords"}))
  })
  -- Author normalization has already run by the pre-AST hook. Refresh the
  -- native template's derived author/affiliation fields after this import.
  doc.meta = require("modules/authors").processAuthorMeta(doc.meta) or doc.meta
  local body = pandoc.Blocks({})
  -- Keep the original author note. The unannotated repeated running title is a
  -- Word title-page convention, and is replaced by the one native title block.
  for i = note_index, keywords_index - 1 do
    local block = blocks[i]
    if block.t == "Header" then
      block.level = 2
      block.classes:insert("unlisted")
      block.classes:insert("unnumbered")
    end
    body:insert(block)
  end
  for i = introduction_index, #blocks do body:insert(blocks[i]) end
  doc.blocks = body
  return doc
end
