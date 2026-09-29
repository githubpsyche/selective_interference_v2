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
    end
  })
end
