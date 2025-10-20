from django.utils.feedgenerator import Rss201rev2Feed


class iTunesFeed(Rss201rev2Feed):
    def rss_attributes(self):
        return {
            "version": self._version,
            "xmlns:atom": "http://www.w3.org/2005/Atom",
            "xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
            "xmlns:content": "http://purl.org/rss/1.0/modules/content/",
            "xmlns:podcast": "https://podcastindex.org/namespace/1.0",
        }

    def add_root_elements(self, handler):
        super().add_root_elements(handler)
        handler.addQuickElement("itunes:subtitle", self.feed["subtitle"])
        handler.addQuickElement("itunes:author", self.feed["author_name"])
        handler.addQuickElement("itunes:summary", self.feed["description"])
        for category in self.feed["itunes_categories"]:
            if isinstance(category, tuple):
                # Handle nested subcategories
                parent, sub = category
                handler.startElement("itunes:category", {"text": parent})
                handler.addQuickElement("itunes:category", "", {"text": sub})
                handler.endElement("itunes:category")
            else:
                handler.addQuickElement("itunes:category", "", {"text": category})

        handler.addQuickElement(
            "itunes:explicit", "true" if self.feed["itunes_explicit"] else "false"
        )
        handler.startElement("itunes:owner", {})
        handler.addQuickElement("itunes:name", self.feed["author_name"])
        handler.addQuickElement("itunes:email", self.feed["author_email"])
        handler.endElement("itunes:owner")
        handler.addQuickElement(
            "itunes:image", "", {"href": self.feed["itunes_image_url"]}
        )

    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)
