import yaml
import xml.etree.ElementTree as xml_tree

#open the feed.yaml file to be read and stored 
#in yaml_data variable
with open('feed.yaml', 'r') as file: 
    yaml_data = yaml.safe_load(file)

#build rss_element using xml_tree
rss_element = xml_tree.Element('rss', {
'version':'2.0',
'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
'xmlns:content':'http://purl.org/rss/1.0/modules/content/'
})

#create the channel element within XML tree
#channel element contains various attributes
#stored inside rss_element as a sub element
channel_element = xml_tree.SubElement(rss_element, 'channel')

#create the header tags that go inside channel tag as a sub elements
#the yaml file has a format that allows for the call on the right
#side of the arrow

link_prefix = yaml_data['link']

xml_tree.SubElement(channel_element, 'title').text = yaml_data['title']
xml_tree.SubElement(channel_element, 'format').text = yaml_data['format']
xml_tree.SubElement(channel_element, 'subtitle').text = yaml_data['subtitle']
xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data['author']
xml_tree.SubElement(channel_element, 'description').text = yaml_data['description']
xml_tree.SubElement(channel_element, 'itunes:image', {'href': link_prefix + yaml_data['image']})
xml_tree.SubElement(channel_element, 'language').text = yaml_data['language']
xml_tree.SubElement(channel_element, 'link').text = link_prefix
xml_tree.SubElement(channel_element, 'itunes:category', {'text': yaml_data['category']})


##creating the item tags that represent the episodes for the podcasts
for item in yaml_data['item']:
    item_element = xml_tree.SubElement(channel_element, 'item')
    xml_tree.SubElement(item_element, 'title').text = item['title']
    xml_tree.SubElement(item_element, 'itunes:author').text = yaml_data['author']
    xml_tree.SubElement(item_element, 'description').text = item['description']
    xml_tree.SubElement(item_element, 'itunes:duration').text = item['duration']
    xml_tree.SubElement(item_element, 'pubDate').text = item['published']

    #enclosure element contains tech info that is useful for podcast RSS feeds
    enclosure = xml_tree.SubElement(item_element, 'enclosure', {
      'url': link_prefix + item['file'],
      'type': 'audio/mpeg',
      'length': item['length']
    })

#after building rss feed, generate a separate file through output tree
output_tree = xml_tree.ElementTree(rss_element)

#write out the output_tree into a podcast.xml file
output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)