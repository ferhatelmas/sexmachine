=========== 
Sex Machine
===========

This package uses the underlying data from the program "gender" by Jorg Michael (described `here <http://www.autohotkey.com/community/viewtopic.php?t=22000>`_).  It's use is pretty straightforward::

    >>> import sexmachine.detector
    >>> d = sexmachine.detector.Detector()
    >>> d.get_gender(u"Bob")
    u'male'
    >>> d.get_gender(u"Sally")
    u'female'
    >>> d.get_gender(u"Pauley") # should be androgynous
    u'andy'

The result will be one of ``andy`` (androgynous), ``male``, ``female``, ``mostly_male``, or ``mostly_female``.  Any unknown names are considered andies.

I18N is fully supported::

    >>> d.get_gender(u"Álfrún")
    u'female'

Additionally, you can give preference to specific countries::

    >>> d.get_gender(u"Jamie")
    u'mostly_female'
    >>> d.get_gender(u"Jamie", u'great_britain')
    u'mostly_male'

If you have an alternative data file, you can pass that in as an optional filename argument to the Detector.  Additionally, you can create a detector that is not case sensitive (default *is* to be case sensitive)::

    >>> d = sexmachine.detector.Detector(case_sensitive=False)
    >>> d.get_gender(u"sally")
    u'female'
    >>> d.get_gender(u"Sally")
    u'female'

Try to avoid creating many Detectors, as each creation means reading in the data file.

Licenses
========

The generator code is distributed under the GPLv3.  The data file nam_dict.txt is released under the GNU Free Documentation License.