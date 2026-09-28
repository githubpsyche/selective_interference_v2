-- This Word import has a literal bibliography, not Pandoc Cite nodes.
-- APAQuarto removes an apparently unused References heading; retain it without
-- moving any manuscript wording or review anchors into metadata.
function Pandoc(doc)
  local has_heading = false
  doc:walk({Header = function(h)
    if h.identifier == "references" then has_heading = true end
  end})
  if has_heading then return doc end
  local restored = false
  return doc:walk({Para = function(p)
    if restored then return nil end
    local reference_entry = false
    p:walk({Span = function(s)
      if s.identifier:match("^ref[-_]") then reference_entry = true end
    end})
    if reference_entry then
      restored = true
      return {pandoc.Header(1, "References", pandoc.Attr("references")), p}
    end
  end})
end
