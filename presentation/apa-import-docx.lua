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
  if not (blocks[1].t == "Header" and keywords and abstract and introduction
      and keywords + 2 == abstract and blocks[abstract - 1].t == "Header") then
    error("The imported APA Word front matter has changed; update apa-import-docx.lua before rendering.")
  end

  local output = pandoc.Blocks({
    pandoc.RawBlock("openxml", '<w:p/><w:p/>'), blocks[1]
  })
  local authors = pandoc.Blocks({})
  for i = 2, (note or keywords) - 1 do authors:insert(blocks[i]) end
  output:insert(styled(authors, "Author"))
  if note then
    output:insert(blocks[note])
    local authornote = pandoc.Blocks({})
    for i = note + 1, keywords - 1 do authornote:insert(blocks[i]) end
    output:insert(styled(authornote, "AuthorNote"))
  end
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
  -- Section membership owns bibliography styling; hyperlink targets do not.
  local references = false
  return doc:walk({
    traverse = "topdown",
    Header = function(h)
      references = pandoc.utils.stringify(h.content) == "References"
    end,
    Para = function(p)
      -- The imported appendix label is bold body text, not a Header node.
      if pandoc.utils.stringify(p) == "Supplementary Material" then references = false end
      if references then return styled({p}, "Bibliography"), false end
      local label = false
      p:walk({Span = function(s)
        if s.identifier:match("^tbl%-") then label = true end
      end})
      if label and pandoc.utils.stringify(p):match("^Table") then
        return styled({p}, "FigureTitle"), false
      end
    end,
    Div = function(d)
      if d.classes:includes("table-note") then
        d.attributes["custom-style"] = "TableNote"
        return d, false
      end
    end
  })
end
