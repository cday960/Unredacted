# Endpoints

# Search and Recent
## /atlas/search/string:search_parameters?int:result_limit&string:start_year&string:end_year
### GET
Search parameters is a string of words separated by + symbols. So to search "john f kennedy", the URL would be `http://unredactedonline.com/atlas/search/john+f+kennedy`

## /atlas/recent/int:result_limit
### GET
Functions similiar to the the previous endpoint `http://unredactedonline.com/atlas/recent/5` but simply pulls the most recently processed documents


## Example Response
```
{
  "data": [
    {
      "digitalObjects": [
        {
          "description": "Reproduction scan of 8x10 transparency",
          "filename": "00303_2003_001_AC.jpg",
          "type": "Image (JPG)",
          "url": "https://s3.amazonaws.com/NARAprodstorage/opastorage/live/51/6677/1667751/content/harvest/1667751-00303/00303_2003_001_AC.jpg"
        },
        {
          "description": "Reproduction scan of 8x10 transparency",
          "filename": "00303_2003_002_AC.jpg",
          "type": "Image (JPG)",
          "url": "https://s3.amazonaws.com/NARAprodstorage/opastorage/live/51/6677/1667751/content/harvest/1667751-00303/00303_2003_002_AC.jpg"
        },
        {
          "description": "Reproduction scan of 8x10 transparency",
          "filename": "00303_2003_003_AC.jpg",
          "type": "Image (JPG)",
          "url": "https://s3.amazonaws.com/NARAprodstorage/opastorage/live/51/6677/1667751/content/harvest/1667751-00303/00303_2003_003_AC.jpg"
        },
        {
          "description": "Reproduction scan of 8x10 transparency",
          "filename": "00303_2003_004_AC.jpg",
          "type": "Image (JPG)",
          "url": "https://s3.amazonaws.com/NARAprodstorage/opastorage/live/51/6677/1667751/content/harvest/1667751-00303/00303_2003_004_AC.jpg"
        },
        {
          "description": "Master Reproduction scan of 8x10 transparency",
          "filename": "00303_2003_001_MA.jpg",
          "type": "Image (JPG)",
          "url": "https://s3.amazonaws.com/NARAprodstorage/opastorage/live/51/6677/1667751/content/harvest/1667751-00303/00303_2003_001_MA.jpg"
        }
      ],
      "doc_type": "_doc",
      "filename": "NAC_2020_Bulk_Desc29008_multi.xml",
      "id": "1667751",
      "title": "Constitution of the United States"
    }
  ]
}
```

# Specific Document
## /atlas/record/id/int:naId
### GET
The `naId` is an ID that is unique to one object of each record type. If trying to retrieve the document from above (id: 1667751), the URL would be `http://unredactedonline.com/atlas/record/id/1667751`. By default it only returns the top result.

## Example Response
```
{
  "data": {
    "digitalObjects": [
      {
        "description": "Reproduction scan of 8x10 transparency",
        "filename": "00303_2003_001_AC.jpg",
        "type": "Image (JPG)",
        "url": "https://s3.amazonaws.com/NARAprodstorage/opastorage/live/51/6677/1667751/content/harvest/1667751-00303/00303_2003_001_AC.jpg"
      },
      {
        "description": "Reproduction scan of 8x10 transparency",
        "filename": "00303_2003_002_AC.jpg",
        "type": "Image (JPG)",
        "url": "https://s3.amazonaws.com/NARAprodstorage/opastorage/live/51/6677/1667751/content/harvest/1667751-00303/00303_2003_002_AC.jpg"
      },
      {
        "description": "Reproduction scan of 8x10 transparency",
        "filename": "00303_2003_003_AC.jpg",
        "type": "Image (JPG)",
        "url": "https://s3.amazonaws.com/NARAprodstorage/opastorage/live/51/6677/1667751/content/harvest/1667751-00303/00303_2003_003_AC.jpg"
      },
      {
        "description": "Reproduction scan of 8x10 transparency",
        "filename": "00303_2003_004_AC.jpg",
        "type": "Image (JPG)",
        "url": "https://s3.amazonaws.com/NARAprodstorage/opastorage/live/51/6677/1667751/content/harvest/1667751-00303/00303_2003_004_AC.jpg"
      },
      {
        "description": "Master Reproduction scan of 8x10 transparency",
        "filename": "00303_2003_001_MA.jpg",
        "type": "Image (JPG)",
        "url": "https://s3.amazonaws.com/NARAprodstorage/opastorage/live/51/6677/1667751/content/harvest/1667751-00303/00303_2003_001_MA.jpg"
      },
      {
        "description": "Master Reproduction scan of 8x10 transparency",
        "filename": "00303_2003_002_MA.jpg",
        "type": "Image (JPG)",
        "url": "https://s3.amazonaws.com/NARAprodstorage/opastorage/live/51/6677/1667751/content/harvest/1667751-00303/00303_2003_002_MA.jpg"
      },
      {
        "description": "Master Reproduction scan of 8x10 transparency",
        "filename": "00303_2003_003_MA.jpg",
        "type": "Image (JPG)",
        "url": "https://s3.amazonaws.com/NARAprodstorage/opastorage/live/51/6677/1667751/content/harvest/1667751-00303/00303_2003_003_MA.jpg"
      },
      {
        "description": "Master Reproduction scan of 8x10 transparency",
        "filename": "00303_2003_004_MA.jpg",
        "type": "Image (JPG)",
        "url": "https://s3.amazonaws.com/NARAprodstorage/opastorage/live/51/6677/1667751/content/harvest/1667751-00303/00303_2003_004_MA.jpg"
      },
      {
        "description": "Download the PDF",
        "filename": "00303.pdf",
        "type": "Portable Document File (PDF)",
        "url": "https://s3.amazonaws.com/NARAprodstorage/opastorage/live/51/6677/1667751/content/arcmedia/congress/00303.pdf"
      }
    ],
    "doc_type": "_doc",
    "filename": "NAC_2020_Bulk_Desc29008_multi.xml",
    "id": "1667751",
    "title": "Constitution of the United States",
    "uuid": "14fd3fa9-dd75-47ae-98e9-a0922378d548"
  }
}
```

