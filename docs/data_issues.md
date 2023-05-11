# point of view

The content we might wish to include is written from a number of points of view. For example guidance pages are written for the public, while tax manuals are written for tax professionals advising others.

This could result in some weirdness, especially when combining knowledge across different types of content!

# search API indexable_content

Have started to spot some cases where there is stuff like 'Top of Page' in the indexable content. Probably not a biggie but may want to check how clean and suitable this source actually is.

# outdated content

Using the query in `sql/duplicate_embeddings.pgsql` we can see that there is lots of duplicated content, which is not useful...

Generally these are notices that say the content is old, out of date, under review, obsolete etc.

For example:

* /hmrc-internal-manuals/capital-gains-manual/cg47883
    * `content: Content archived, see CG10100`
* /hmrc-internal-manuals/capital-gains-manual/cg72384
    * `content: Merged with CG72380. Page archived.`
* /hmrc-internal-manuals/company-taxation-manual/ctm04500
    * `content:`
* /hmrc-internal-manuals/compliance-operational-guidance/cog103485
    * `content: (This content has been withheld because of exemptions in the Freedom of Information Act 2000)`
* /hmrc-internal-manuals/international-manual/intmupdate100713
    * `content: Page archived – Old legacy update page no longer required`
* /hmrc-internal-manuals/compliance-operational-guidance/cog905160
    * `content: This guidance has been removed following a review of its content revealed it is now obsolete.`
* /hmrc-internal-manuals/cap-imports/capi13000
    * `content: Note: This manual is currently under review following Brexit. Some content may be withdrawn or revised during this process. If there is anything within this manual you use regularly, please email hmrcmanualsteam@hmrc.gov.uk to let us know. In the meantime, you should check the other guidance available on GOV.UK from HMRC.`

The search API has an `is_withdrawn` field but it doesnt look like its being used.

`https://www.gov.uk/api/search.json?filter_link=/hmrc-internal-manuals/capital-gains-manual/cg47883&fields=is_withdrawn`

Similarly, the content API has a `withdrawn` flag in a few places, but this doesnt seem to be set to TRUE for the above, so not useful here.

So - best approach is probably to dedupe the pulled data.