-- Correct the imported Word outline for HTML navigation only.
-- Keep the pooled QMD, its prose, review anchors, and the frozen source intact.
function Pandoc(doc)
  if not quarto.doc.is_format("html") then return nil end
  local in_front_matter = not doc.meta["review-import-front-matter"]
  return doc:walk({
    traverse = "topdown",
    Header = function(h)
      local text = pandoc.utils.stringify(h.content)
      if text == "Abstract" then in_front_matter = false end
      if in_front_matter and h.level == 1 then
        h.classes:insert("unlisted")
        h.classes:insert("unnumbered")
        return h
      end
      -- The source Word file assigns Heading 2 to this body paragraph.
      if h.level == 2 and text:match("^A dual%-list externalized free%-recall design would isolate these predictions") then
        return pandoc.Para(h.content)
      end
    end,
    Para = function(p)
      -- Its actual section label is bold text in the Word source.
      if #p.content == 1 and p.content[1].t == "Strong"
          and pandoc.utils.stringify(p.content) == "Testing Competitor Learning and Retrieval Selectivity" then
        return pandoc.Header(2, p.content[1].content,
          pandoc.Attr("testing-competitor-learning-and-retrieval-selectivity"))
      end
    end
  })
end
