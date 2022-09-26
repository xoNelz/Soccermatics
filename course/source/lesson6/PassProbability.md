Pass probability
================

There is different alternative ways of measuring which player has control over which part of the pitch. Many of
these build on the probability a pass is successful.

### Overview of pitch control and passing models

Pitch control is the probability that a player could control the ball assuming it is at that location. William Spearman explains: 
- the principles behind pitch control models 
- how they can be used to investigate player positioning
- how to extend them to account for ball motion. 
- How to combine pitch control models with measures of expected threat (see lesson 7)
- defines 'off-ball scoring opportunity'

<iframe width="640" height="480" src="https://www.youtube.com/embed/X9PrwPyolyU" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>



### Further reading

Pitch control demo: </span><a class="yt-simple-endpoint style-scope yt-formatted-string" href="https://www.youtube.com/redirect?v=X9PrwPyolyU&amp;redir_token=QUFFLUhqblFaTkcySl9aaHdvOEhIanFLWWpidjN2a3k0UXxBQ3Jtc0tuZ1MtMFdHVHZWTHN1ZHBLanczQXA4ZFN5dGNpcUREd3pEZjhaWmFTNVU4ZlZBSnItbDBfU3BWM1M3UUxKLWs4SlRZTGt5X1A4SVFFZ2Z5MjROUWJxQllSdmYwOTAya3dBQkRCRVNjVDkxZ1JYUmhadw%3D%3D&amp;event=video_description&amp;q=https%3A%2F%2Fhudl.com%2Fblog%2Fopen-space-and-passing-in-football" target="_blank" rel="noopener">https://hudl.com/blog/open-space-and-...</a></p>
<p><span class="style-scope yt-formatted-string">Quantifying Pitch Control: </span><a class="yt-simple-endpoint style-scope yt-formatted-string" href="https://www.youtube.com/redirect?v=X9PrwPyolyU&amp;redir_token=QUFFLUhqbm9MLXhDRlV2OWRFakFtVHFHaXkwRl9hRW8wQXxBQ3Jtc0tuaWlSbnlqYXJMUFNGMTNhODZSYVFSMEhFVktGOWxXSmx4XzBfempuRzQ2TUVaQi1uVWFUcmRLaTkxYTVlb2gzRVFBQWZvVmRWMTI5Qk5KcTM0SUw5ZTZwdUM1d0FldFVIdEItb1F4czFibUItVDd2aw%3D%3D&amp;event=video_description&amp;q=https%3A%2F%2Fresearchgate.net%2Fpublication%2F334849056_Quantifying_Pitch_Control" target="_blank" rel="noopener">https://researchgate.net/publication/...</a></p>
<p><span class="style-scope yt-formatted-string">Physics-Based Modeling of Pass Probabilities in Soccer: </span><a class="yt-simple-endpoint style-scope yt-formatted-string" href="https://www.youtube.com/redirect?v=X9PrwPyolyU&amp;redir_token=QUFFLUhqbGdXaC1QNXB2eEpITzk1T2VnM2t6WHVSZE5iQXxBQ3Jtc0tsX2RjTUE5RjJHZ2dOcEhkdkh2RS1XZnhRLVpKbHRGMklBYTRiRjJsQjhudFpuVnJRc3RMejRKUXIxdEJzRTlfbHlJOXBnV2JMUjI5cWRMSlZwaXpHeGdCSWRRMDJsYXlWcnJIWnZyd3lnc25CZUFaMA%3D%3D&amp;event=video_description&amp;q=https%3A%2F%2Fresearchgate.net%2Fpublication%2F315166647_Physics-Based_Modeling_of_Pass_Probabilities_in_Soccer" target="_blank" rel="noopener">https://researchgate.net/publication/...</a></p>
<p><span class="style-scope yt-formatted-string">Wide Open Spaces: A statistical technique for measuring space creation in professional soccer: </span><a class="yt-simple-endpoint style-scope yt-formatted-string" href="https://www.youtube.com/redirect?v=X9PrwPyolyU&amp;redir_token=QUFFLUhqbTRuSGp2N3U0Ykp2N1hJdXhvZW52T1JWb1lnd3xBQ3Jtc0ttN2tZd0oxd2YtZXJkTkVYa29pd2VCRU12ejRoODh1eUFBYjU2WHZhcEdqZXc2aVctdVNZNHlqa3JYYVZRRWtfaGEwcUpqc1c1ZmsyVEdJS3daMjFzRXdQTUtpQ3c3VlZxRkRIanhvY2RSMnZjOXVqRQ%3D%3D&amp;event=video_description&amp;q=https%3A%2F%2Fresearchgate.net%2Fpublication%2F324942294_Wide_Open_Spaces_A_statistical_technique_for_measuring_space_creation_in_professional_soccer" target="_blank" rel="noopener">https://researchgate.net/publication/...</a></p>

### Implementing a pitch control model

Laurie Shaw describes everything you need to create a pitch control model in Python.

<iframe width="640" height="480" src="https://www.youtube.com/embed/5X1cSehLg6s" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<p><span class="style-scope yt-formatted-string">Code for this tutorial can be found here: </span><a class="yt-simple-endpoint style-scope yt-formatted-string" href="https://www.youtube.com/redirect?event=video_description&amp;v=KXSLKwADXKI&amp;redir_token=QUFFLUhqbUVpOTN3bVcwUHlLV3pxLWJBenlkbFRsMVhXd3xBQ3Jtc0tuUzRQREJXMWNjZ3otdEY4YTBXb2VodDZ2bW4tTGs4eDFEcjFwWlFOS2pzZzBEWFBlY2dZa1hkcTFJdllrZC00YUl5MGVWRDBtUHp4akh3cVhxY1MyZHBhazJ4eXlJdEU0LWlkUU1ETjl3V3liRk1Haw%3D%3D&amp;q=https%3A%2F%2Fgithub.com%2FFriends-of-Tracking-Data-FoTD%2FLaurieOnTracking" target="_blank" rel="noopener">https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking</a></p>

<p><span class="style-scope yt-formatted-string">Data used in this tutorial can be found here: </span><a class="yt-simple-endpoint style-scope yt-formatted-string" href="https://www.youtube.com/redirect?event=video_description&amp;v=KXSLKwADXKI&amp;redir_token=QUFFLUhqbk02RUlrZHV0U2RfY2J1WTdjdzcyVGNzZXZ1Z3xBQ3Jtc0tsRzF1cXdVZWhUOXNwaWJUaEV5TUdrX1A5aWFreGxqa3ZXQ1hsQkh6eUp5RkdRLW5yMzBxSmlhOGozOVM3U29VZzM3TGFFaWhtb2VoQklyQXIyQ1FWb1FQVUVtWFVCdU5PZ2tfVm9SampvYm02UVc1RQ%3D%3D&amp;q=https%3A%2F%2Fgithub.com%2Fmetrica-sports%2Fsample-data" target="_blank" rel="noopener">https://github.com/metrica-sports/sample-data</a></p>



