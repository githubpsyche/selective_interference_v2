-- Map the imported Word front matter to APAQuarto's own Word styles. Keep the
-- annotated title occurrences separate: rebuilding either from plain metadata
-- would lose its native review anchors or duplicate a suggestion identity.
if FORMAT ~= "docx" then return end

local function styled(blocks, name)
  return pandoc.Div(blocks, pandoc.Attr("", {}, {["custom-style"] = name}))
end

local function pagebreak()
  return pandoc.RawBlock("openxml", '<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
end

function Pandoc(doc)
  local blocks = doc.blocks
  local note, keywords, abstract, introduction
  for i, block in ipairs(blocks) do
    local text = pandoc.utils.stringify(block)
    if block.t == "Header" then
      if text == "Author Note" then note = i end
      if text == "Abstract" then abstract = i end
      if text == "Introduction" then introduction = i; break end
    elseif block.t == "Para" and text:match("^Keywords:") then
      keywords = i
    end
  end
  if not (blocks[1].t == "Header" and note and keywords and abstract and introduction
      and keywords + 2 == abstract and blocks[abstract - 1].t == "Header") then
    error("The imported APA Word front matter has changed; update apa-import-docx.lua before rendering.")
  end

  local output = pandoc.Blocks({
    pandoc.RawBlock("openxml", '<w:p/><w:p/>'), blocks[1]
  })
  local authors = pandoc.Blocks({})
  for i = 2, note - 1 do authors:insert(blocks[i]) end
  output:insert(styled(authors, "Author"))
  output:insert(blocks[note])
  local authornote = pandoc.Blocks({})
  for i = note + 1, keywords - 1 do authornote:insert(blocks[i]) end
  output:insert(styled(authornote, "AuthorNote"))
  output:insert(pagebreak())
  output:insert(blocks[abstract])
  for i = abstract + 1, introduction - 1 do
    output:insert(styled({blocks[i]}, i == abstract + 1 and "AbstractFirstParagraph" or "Abstract"))
  end
  output:insert(styled({blocks[keywords]}, "Body Text"))
  output:insert(pagebreak())
  output:insert(blocks[abstract - 1])
  for i = introduction, #blocks do output:insert(blocks[i]) end
  doc.blocks = output

  -- This import contains literal reference entries rather than Cite nodes.
  -- Assign the template's hanging-indent style without rebuilding their text.
  return doc:walk({Para = function(p)
    local reference = false
    p:walk({Span = function(s)
      if s.identifier:match("^ref[-_]") then reference = true end
    end})
    if reference then return styled({p}, "Bibliography") end
  end})
end
