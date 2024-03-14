# Endpoints
## /webapp/search/\<string:search_parameters\>
#### GET Request
Search parameters is a string of words separated by + symbols. So to search "john f kennedy", the URL would be `http://127.0.0.1/webapp/search/john+f+kennedy`

### /webapp/search/\<string:search_parameters\>/\<int:result_limit\>
Functions the same as the previous endpoint except you can add a `result_limit` parameter that limits the number of results that are returned (surprise!). So to limit the john f kennedy search to 10 results, the url would be `http://127.0.0.1/webapp/search/john+f+kennedy/10`

#### Example Response
```
{
  "data": [
    {
      "date": "2022-11-16 20:48:58.845780",
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

## /webapp/records/id/\<string:naId\>
#### GET Request
The `naId` is an ID that is unique to one object of each record type. If trying to retrieve the document from above (id: 1667751), the URL would be `http://127.0.0.1:5000/webapp/records/id/1667751`. By default it only returns the top result.

#### Example Response
```
{
  "data": {
    "date": "2022-11-16 20:48:58.845780",
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

